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
            content=f'Webhook received: {event["type"]}',
            status=200)
