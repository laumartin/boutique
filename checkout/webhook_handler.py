from django.http import HttpResponse

from .models import Order, OrderLineItem
from products.models import Product

import json
import time

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
        """
        in case the form isn't submitted for some reason(user closes the
        page on the loading screen.Get the payment intent id, the shopping
        bag and the users save info preference from the metadata we added.
        """
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)
        # to ensure the data is in the same form as what we want in our db
        # replace any empty strings in the shipping details with none.
        # Since stripe will store them as blank strings which is not the
        # same as the null value we want in the database
        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # let's assume order doesn't exist
        order_exists = False
        # Instead of just immediately create the order if it's not
        # found in the database introduce a bit of delay:
        attempt = 1
        while attempt <= 5:
            try:
                # try to get the order using all the information from the
                # payment intent.using the iexact field to make it an exact
                # match but case-insensitive
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    stret_Address1__iexact=shipping_details.address.line1,
                    stret_Address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total__iexact=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                # If the order is found set order exists to true,and return
                # 200 HTTP response to stripe, with message that we verified
                # the order already exists.
                order_exists = True
                break
            except Order.DoesNotExist:
                # instead of creating order if it's not found the first time
                # increment attempt by 1 then use pythons time module to
                # sleep for 1second.This will cause webhook handler to try to
                # find the order 5 times over 5 seconds from the while loop
                # before giving up and creating the order itself.
                attempt += 1
                time.sleep(1)
        if order_exists:
            return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                    status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                        full_name=shipping_details.name,
                        email=billing_details.email,
                        phone_number=shipping_details.phone,
                        country=shipping_details.address.country,
                        postcode=shipping_details.address.postal_code,
                        town_or_city=shipping_details.address.city,
                        stret_Address1=shipping_details.address.line1,
                        stret_Address2=shipping_details.address.line2,
                        county=shipping_details.address.state,
                        original_bag=bag,
                        stripe_pid=pid,
                    )
                    # we get the Product ID out of the bag
                for item_id, item_data in json.loads(bag).items():
                        product = Product.objects.get(id=item_id)
                        # if its value is integer we know is an item that doesn't
                        # have sizes.So quantity will be the item data.
                        if isinstance(item_data, int):
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=item_data,
                            )
                            order_line_item.save()
                        else:
                            # if the item has sizes iterate through each size
                            # and create a line item accordingly.
                            for size, quantity in item_data['items_by_size'].items():
                                order_line_item = OrderLineItem(
                                    order=order,
                                    product=product,
                                    quantity=quantity,
                                    product_size=size,
                                )
                                order_line_item.save()
            except Exception as e:
                # if anything goes wrong delete the order if it was created
                # return a 500 server error response to stripe.This will cause
                # stripe to automatically try the webhook again later.
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)


        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from stripe.
        This will be sent each time a user completes the payment process.
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
