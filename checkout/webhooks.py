# settings file to get the webhook and the stripe API secrets.
# We need HttpResponse so these exception handlers will work.
from django.conf import settings
from django.http import HttpResponse
# will make this view require a post request and reject get requests.
from django.views.decorators.http import require_POST
# stripe won't send a CSRF token like we'd normally need.
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import StripeWH_Handler

import stripe


@require_POST
@csrf_exempt
def webhook(request):
    """Listen for webhooks from Stripe"""
    # Setup
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Get the webhook data and verify its signature
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    except Exception as e:
        return HttpResponse(content=e, status=400)


# Set up a webhook handler
    handler = StripeWH_Handler(request)

    # create a dictionary. the dictionaries keys will be the names
    # of the webhooks coming from stripe.its values will be the actual
    # methods inside handler.Map webhook events to relevant handler functions
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    # Get the webhook type from Stripe
    event_type = event['type']

    # If there's a handler for it, get it from the event map
    # Use the generic one by default.
    # we'll look up the key in dictionary,assign its value to a variable
    # called event handler. event handler is nothing more than an alias for
    # whatever function we pulled out of the dictionary.we can call it just
    # like any other function
    event_handler = event_map.get(event_type, handler.handle_event)

    # Call the event handler with the event
    response = event_handler(event)
    return response
