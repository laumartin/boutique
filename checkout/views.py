from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    # get the bag from the session.
    bag = request.session.get('bag', {})
    # if there's nothing in the bag just add error message and redirect
    # back to products page
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51IOUA7G0x4S4dim32Wd4GJCyL0yXABEY8C70buH0iuGdds3nwHRDyp92NajoqECCcwkF7ugyUUap8lsF1y7rRv6Y00ZqzgRAs1',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
