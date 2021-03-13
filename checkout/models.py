import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from products.models import Product
# Create your models here to create and track orders for anyone who makes a purchase.


class Order(models.Model):

    # automatically generate this order number editable=false
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    # automatically set order date and time whenever a new order is created.
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    # if a customer purchase the same things twice on separate occasions it
    # would result in us finding the first order in the db when they place
    # the second one and thus the second-order never being added.To avoid 
    # add two new fields to the order model.The first is a text field that
    # will contain the original shopping bag that created it.And the 2nd is
    # a character field that will contain the stripe payment intent unique id
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

# prepended with an underscore by convention to indicate it's a
# private method which will only be used inside this class.
    def _generate_order_number(self):
        """ Generate a random, unique order number using UUID will just
        generate a random string of 32 characters to use as order number."""
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """ 
        Update grand total each time a line item is added, accounting
        for delivery costs. it has method to update the total which we
        can do using the aggregate function. The way this works is by using
        the sum function across all the line-item total fields for all line
        items on this order.The default behaviour is to add a new field to
        the query set called line-item total sum which we can then get and
        set the order total to that."""
        # or 0 at the end aggregates all the line item totals, preventing
        # an error if we manually delete line items form an order, this
        # sets total to zero instead of none.
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        # calculate delivery cost using the free delivery threshold and
        # the standard delivery percentage from settings file. Setting it
        # to zero if the order total is higher than the threshold.
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0
            # to calculate grand total,add the order total and the delivery
            # cost together and save the instance.
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """ Override the original save method to set the order number
        if it hasn't been set already. if the order we're saving right
        now doesn't have an order number call the generate order number
        method and execute the original save method."""

        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


# A line-item will be like an individual shopping bag item.
# Relating to a specific order
# when a user checks out we'll first use the information they
# put into the payment form to create an order instance, then
# iterate through the items in the shopping bag creating an order
# line item for each one. Attaching it to the order and updating
# the delivery cost, order total, and grand total along the way
# on the order line item model.
class OrderLineItem(models.Model):
    # There's a foreign key to the order with a related name of
    # line items so when accessing orders we'll be able to make
    # calls such as order.lineitems.all and order.lineitems.filter
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    # There's also a foreign key to the product for this line item
    # so we can access all the fields of the associated product.
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2, null=True, blank=True) # XS, S, M, L, XL
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)


    # Like setting the order number on the order model we also need to
    # set the line-item total field on the order line-item model by
    # overriding its save method.We just need to multiply the product
    # rice by the quantity for each line item.

    def save(self, *args, **kwargs):
        """
        Override original save method to set the lineitem
        total and update the order total
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
