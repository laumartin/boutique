# basic process is that will first create an order.Then iterate through
# shopping bag adding line items to it one by one updating the various
# costs along the way. We've got the method to update the total already in
# the order model,just need a way to call it each time a line item is attached
# to the order for that we'll use a built-in feature of django, signals.
# Post implies these signals are sent by django to the entire application
# after a model instance is saved and after it's deleted respectively.
from django.db.models.signals import post_save, post_delete
# To receive these signals we can import receiver from django.dispatch.
from django.dispatch import receiver

# since we'll be listening for signals from the OrderLineItem model
from .models import OrderLineItem


# to execute this function anytime the post_save signal is sent
# use the receiver decorator. Telling it we're receiving post saved signals
# from the OrderLineItem model.
@receiver(post_save, sender=OrderLineItem)
# this function which will handle signals from the post_save event.
# So these parameters refer to the sender of the signal, OrderLineItem.
def update_on_save(sender, instance, created, **kwargs):

    # update order total on lineitem update/create. we just have to access
    # instance.order which refers to the order this specific line item is
    # related to and call the update_total method on it
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    instance.order.update_total()
