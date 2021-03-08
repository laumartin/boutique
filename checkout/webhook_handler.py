from django.http import HttpResponse


class StripeWH_Handler:
    """Handle Stripe webhooks
    The init method of the class is a setup method called every
    time an instance of the class is created.we're going to use it
    to assign the request as an attribute of the class
"""

    def __init__(self, request):
        self.request = request

# create a class method called handle event which will take the event
# stripe is sending us and return an HTTP response indicating it was received.
    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from stripe.
        This will be sent each time a user completes the payment process.
        """
        intent = event.data.object
        print(intent)
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from stripe.
        This will be sent each time a user completes the payment process.
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
