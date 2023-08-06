import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.signing import BadSignature
from django.db import transaction
from django.forms.models import formset_factory
from django.http import (
    Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect)
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, TemplateView

from wafer.registration.views import redirect_profile

from stripe import Webhook
from stripe.error import AuthenticationError, SignatureVerificationError

from invoices.forms import CombineForm, InvoiceForm, InvoiceFormset
from invoices.models import Invoice, InvoiceLine
from invoices.stripe_payments import (
    charge_refunded, dispute_filed, payment_intent_succeeded)
from register.models import Attendee

log = logging.getLogger(__name__)


class InvoiceDetailView(DetailView):
    model = Invoice
    slug_field = 'reference_number'
    slug_url_kwarg = 'reference_number'

    def get_object(self):
        invoice = super().get_object()

        if self.can_view_invoice(invoice):
            return invoice

        raise Http404()

    def can_view_invoice(self, invoice):
        user = self.request.user
        return (user.has_perm('front_desk.change_checkin')
                or invoice.recipient == user)

    def can_cancel_invoice(self, invoice):
        user = self.request.user
        return (user.has_perm('front_desk.change_invoice')
                or invoice.recipient == user)


class InvoiceDisplay(InvoiceDetailView):
    template_name = 'invoices/invoice_detail.html'

    def get_object(self):
        self.unsign()
        return super().get_object()

    def unsign(self):
        reference_number = self.kwargs['reference_number']
        self.using_signed_url = ':' in reference_number
        if self.using_signed_url:
            try:
                reference_number = Invoice.signer.unsign(reference_number)
            except BadSignature:
                raise Http404()
            self.kwargs['reference_number'] = reference_number

    def can_view_invoice(self, invoice):
        return self.using_signed_url or super().can_view_invoice(invoice)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        if self.object.status == 'new':
            try:
                payment_intent = self.object.get_payment_intent()
                payment_intent_client_secret = payment_intent.client_secret
            except AuthenticationError:
                log.error('Stripe authentication error. '
                          'Is STRIPE_ENDPOINT_SECRET set?')
                payment_intent_client_secret = ''

            context_data.update({
                'payment_intent_client_secret': payment_intent_client_secret,
                'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
            })

        context_data.update({
            'using_signed_url': self.using_signed_url,
            'DEBCONF_CITY': settings.DEBCONF_CITY,
            'DEBCONF_LOCAL_CURRENCY': settings.DEBCONF_LOCAL_CURRENCY,
            'DEBCONF_NAME': settings.DEBCONF_NAME,
        })

        return context_data


class InvoiceCancel(LoginRequiredMixin, InvoiceDetailView):

    @transaction.atomic
    def post(self, request, **kwargs):
        invoice = self.get_object()
        if not self.can_cancel_invoice(invoice):
            raise PermissionDenied()

        if invoice.status == 'new':
            invoice.status = 'canceled'
            invoice.save()
            messages.success(
                self.request, 'Invoice cancelled')
        else:
            messages.warning(
                self.request, 'Only unpaid invoices can be cancelled')

        return redirect_profile(self.request)


class FormFormsetView(TemplateView):
    def get_initial(self):
        return {}

    def get_initial_formset(self):
        return []

    def get_form_kwargs(self):
        kwargs = {
            'initial': self.get_initial(),
        }
        if self.request.method == 'POST':
            kwargs['data'] = self.request.POST
        return kwargs

    def get_form(self):
        return self.form_class(**self.get_form_kwargs())

    def get_formset_kwargs(self):
        kwargs = {
            'form_kwargs': self.get_formset_form_kwargs(),
        }
        if self.request.method == 'POST':
            kwargs['data'] = self.request.POST
        else:
            kwargs['initial'] = self.get_initial_formset()
        return kwargs

    def get_formset_form_kwargs(self):
        return {}

    def get_formset(self):
        Formset = formset_factory(
            self.formset_form_class, formset=self.formset_class, extra=2)
        return Formset(**self.get_formset_kwargs())

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        if 'formset' not in kwargs:
            kwargs['formset'] = self.get_formset()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        formset = self.get_formset()
        if form.is_valid() and formset.is_valid():
            return self.forms_valid(form, formset)
        else:
            return self.forms_invalid(form, formset)

    def forms_valid(self, form, formset):
        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form, formset):
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset))


class InvoiceCombine(LoginRequiredMixin, FormFormsetView):
    template_name = 'invoices/combine.html'
    form_class = CombineForm
    formset_form_class = InvoiceForm
    formset_class = InvoiceFormset

    def get_initial(self):
        user = self.request.user
        initial = {
            'invoiced_entity': user.userprofile.display_name()
        }
        try:
            attendee = user.attendee
        except Attendee.DoesNotExist:
            pass
        else:
            initial['billing_address'] = attendee.billing_address
        return initial

    def get_initial_formset(self):
        return [{'url': url}
                for i, url in enumerate(self.request.GET.getlist('invoice'))]

    def get_formset_form_kwargs(self):
        return {
            'user': self.request.user,
        }

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def forms_valid(self, form, formset):
        user = self.request.user

        invoice = Invoice(
            recipient=user,
            status='new',
            compound=True,
            date=timezone.now(),
            invoiced_entity=form.cleaned_data['invoiced_entity'],
            billing_address=form.cleaned_data['billing_address'],
        )
        invoice.save()

        for i, form in enumerate(formset.forms):
            if not hasattr(form, 'invoice'):
                continue
            child_invoice = form.invoice
            InvoiceLine(
                invoice_id=invoice.id,
                line_order=i,
                reference='INV#{}'.format(child_invoice.reference_number),
                description='DebConf attendance for {}'.format(
                    child_invoice.recipient.userprofile.display_name()
                ),
                unit_price=child_invoice.total,
                quantity=1,
            ).save()

        self.reference_number = invoice.reference_number
        return super().forms_valid(form, formset)

    def get_success_url(self):
        return reverse('invoices:display',
                       kwargs={'reference_number': self.reference_number})


@csrf_exempt
def stripe_webhook(request):
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    try:
        event = Webhook.construct_event(
            request.body, sig_header, settings.STRIPE_ENDPOINT_SECRET)
    except ValueError:
        return HttpResponseBadRequest("Invalid event")
    except SignatureVerificationError:
        return HttpResponse(status=400)
    if event.type == 'payment_intent.succeeded':
        intent = event.data.object
        payment_intent_succeeded(intent, ignore_unrelated=True)
    elif event.type == 'charge.dispute.created':
        dispute = event.data.object
        dispute_filed(dispute, ignore_unrelated=True)
    elif event.type == 'charge.refunded':
        charge = event.data.object
        charge_refunded(charge, ignore_unrelated=True)
    else:
        return HttpResponse(status=400)
    return HttpResponse(status=204)
