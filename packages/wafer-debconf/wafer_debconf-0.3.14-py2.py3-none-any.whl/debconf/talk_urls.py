from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

from rest_framework import serializers

from wafer.talks.models import Talk, TalkUrl
from wafer.talks.serializers import TalkSerializer, TalkUrlSerializer


def provision_urls_setting():
    """Lookup the DEBCONF_TALK_PROVISION_URLS setting"""
    return getattr(settings, 'DEBCONF_TALK_PROVISION_URLS', {})


def create_online_service_urls(talk, regenerate=False):
    """Generate URLs for any online services associated with the Talk

    e.g. Jitsi Meet rooms or Etherpads
    """
    for key, config in provision_urls_setting().items():
        if talk.urls.filter(description=key).exists() and not regenerate:
            continue
        url = config['pattern'].format(
            id=talk.talk_id,
            slug=talk.slug,
            secret16=get_random_string(length=16))
        TalkUrl.objects.update_or_create(
            talk=talk,
            description=key,
            defaults={'url': url})


@receiver(post_save, sender=Talk)
def create_online_service_urls_reciever(sender, **kwargs):
    talk = kwargs['instance']
    if talk.accepted:
        create_online_service_urls(talk)


# Monkey-patch the TalkUrl serializer in wafer, to hide these URLs in the
# (public) talk API
# Remove once https://github.com/CTPUG/wafer/pull/545 has landed
class TalkUrlListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        private_keys = [
            key for key, config in provision_urls_setting().items()
            if config['private']]
        data = data.exclude(description__in=private_keys)
        return super().to_representation(data)

TalkSerializer._declared_fields['urls'] = TalkUrlListSerializer(
    child=TalkUrlSerializer(read_only=True), read_only=True)
