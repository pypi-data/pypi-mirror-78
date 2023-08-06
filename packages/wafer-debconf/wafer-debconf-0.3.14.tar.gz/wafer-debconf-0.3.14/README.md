# Wafer apps for DebConf

This package contains several Django apps used by the DebConf
conference.

## badges - Name tag generation

## bursary - Bursary requests and review

## debconf - Random bits and pieces

## front\_desk - Check-In

## invoices - Paid Attendee Invoicing

## register - Attendee Registration

## volunteers - On-site volunteer wrangling

# Configuration

Uses the following Django settings:

Invoicing:

* `DEBCONF_LOCAL_CURRENCY_RATE`: Decimal. The exchange rate. What does $1 USD buy in local currency.
* `DEBCONF_LOCAL_CURRENCY_SYMBOL`: String. The local currency symbol.
* `DEBCONF_LOCAL_CURRENCY`: String. The local currency code.
* `INVOICE_PREFIX`: String. Prefix to invoice IDs.
* `PRICES`: Dict of Dicts, with purchasable items and prices.
  * `fee`: Dict of conferences fees, each having a `name` and `price`.
  * `meal`: Dict of Dicts, (`breakfast`, `lunch`, `dinner`, `conference_dinner`):
    * Each having a `price` and optional `name`.
  * `accomm`: Dict with one key: `price` (per night).
* `STRIPE_PUBLISHABLE_KEY`: String. Stripe API Publishable Key.
* `STRIPE_SECRET_KEY`: String. Stripe API Secret Key.
* `STRIPE_ENDPOINT_SECRET`: String. Stripe Webhook endpoint secret.

Dates:

* `DEBCONF_BURSARY_DEADLINE`: Date. The date that bursaries need to be submitted by.
* `DEBCONF_BURSARY_ACCEPTANCE_DEADLINE`: Date. The date that all bursaries need to be accepted by, or the attendee will be issued an invoice.
* `DEBCONF_CONFERENCE_DINNER_DAY`: Date. The day that has the conference dinner.
* `DEBCONF_CONFIRMATION_DEADLINE`: Date. The date that attendance needs to be confirmed by.
* `DEBCONF_DATES`: List of (Description, Start Date, End Date) for the parts of the conference.
* `VOLUNTEERS_FIRST_DAY`: Date. The first day of volunteering.
* `VOLUNTEERS_LAST_DAY`: Date. The last day of volunteering.

Registration:

* `BURSARIES_CLOSED`: Boolean. Can bursary requests still be submitted.
* `DEBCONF_BREAKFAST`: Boolean. Is DebConf providing breakfast for attendees.
* `DEBCONF_PAID_ACCOMMODATION`: Boolean. Is DebConf providing accommodation for self-paying attendees.
* `DEBCONF_SHOE_SIZES`: List of (Key, Description) for Shoe sizes.
* `DEBCONF_T_SHIRT_SIZES`: List of (Key, Description) for T-Shirt sizes.
* `RECONFIRMATION`: Boolean. Is there a reconfirmation round.

Content:

* `TRACKS_FILE`: String. path to a YAML file with the list of tracks to be loadede into the database
* `TALK_TYPES_FILE`: String. path to a YAML file with the list of talk types to be loaded into the database
* `DEBCONF_TALK_PROVISION_URLS`: Dictionary of {Key: {pattern: String, private: Boolean}} for online services to generate links for. Format string parameters available: `id`, `slug`, `secret16`).

Misc:

* `DEBCONF_CITY`: String. The name of the city hosting DebConf.
* `DEBCONF_NAME`: String. The name of the Debconf (e.g. "DebConf XX").
* `DCSCHEDULE_TOKEN`: String. Authentication token for the DCSchedule IRC bot to hit the API.
* `SANDBOX`: Boolean. Is this a development instance or production.
* `ISSUE_KSP_ID`: Boolean. Is the key-signing sign-up still open?

## Stripe Payments

First, configure the `STRIPE_PUBLISHABLE_KEY` and `STRIPE_SECRET_KEY`
settings, with the API keys from the Stripe dashboard.

To receive payment confirmation from Stripe, we need to receive a
webhook from them.

For local development, you can receive this with the [stripe
CLI](https://github.com/stripe/stripe-cli):

```
$ stripe login
...
$ stripe listen --forward-to http://127.0.0.1:8000/invoices/stripe-webhook/
> Ready! Your webhook signing secret is whsec_I_AM_A_SECRET_KEY (^C to quit)
```

Configure `STRIPE_ENDPOINT_SECRET` with the secret key provided by
`stripe-cli listen`.

For production use, configure a webhook in the Stripe dashboard.
The endpoint should be `https://my.debconf/invoices/stripe-webhook/`.
Listen for `charge.dispute.created`,  `charge.refunded`, and
`payment_intent.succeeded`.
Again, `STRIPE_ENDPOINT_SECRET` should be configured to the webhook's
signing secret.
