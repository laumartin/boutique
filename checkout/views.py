from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
# all that function returns is a Python dictionary.
from bag.contexts import bag_contents

import stripe
import json


# before we call the confirm card payment method in the stripe JavaScrip.
# we'll make a post request to this view and give it the client secret
# from the payment intent.
@require_POST
def cache_checkout_data(request):
    try:
        # first part is payment intent Id,store that in a variable called pid.
        pid = request.POST.get('client_secret').split('_secret')[0]
        # Then I'll set up stripe with the secret key so we can modify the
        # payment intent.
        stripe.api_key = settings.STRIPE_SECRET_KEY
        # To do it, call stripe.PaymentIntent.modify give it the pid, and
        # tell it what we want to modify in our case we'll add some metadata.
        stripe.PaymentIntent.modify(pid, metadata={
            # add the user who's placing the order.add whether or not they
            # want to save their info and add a JSON dump of shopping bag
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # check whether the method is post.
    if request.method == 'POST':
        # get the bag from the session.then put the form data in a dictionary
        bag = request.session.get('bag', {})

        form_data = {
            # we can create an instance of the form using the form data.
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        # If the form is valid we'll save the order.
        # then we iterate through the bag items to create each line item.
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            # prevent multiple save events from being executed on the database
            # by adding commit=false to prevent the 1st one from happening.
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()
            for item_id, item_data in bag.items():
                try:
                    # we get the Product ID out of the bag
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
                # in case a product isn't found add error message Delete empty
                # order and return the user to the shopping bag page.
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))
            # We'll attach whether or not the user wanted to save their profile
            # information to the session.
            request.session['save_info'] = 'save-info' in request.POST
            # redirect them to a new page and pass the order number as argument
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        bag = request.session.get('bag', {})

        # if there's nothing in the bag just add error message and redirect
        # back to products page
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('products'))

    # We can pass the request and get the same dictionary here in the view.
    # store that in a variable called current bag.Making sure not to overwrite
    # the bag variable that already exists
        current_bag = bag_contents(request)
    # get the grand_total key out of the current bag.
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
        # Since users now have profiles we can use their default delivery info
        #  to pre-fill the form on the checkout page by checking whether user
        # is authenticated,if so, get their profile and use the initial
        # parameter on the order form to pre-fill all its fields
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


# This take the order number and render a success page letting the user
# know that their payment is complete.
def checkout_success(request, order_number):
    # first check whether the user wanted to save their information
    # by getting that from the session
    save_info = request.session.get('save_info')
    # use the order number to get the order created in the previous view
    # which we'll send back to the template
    order = get_object_or_404(Order, order_number=order_number)

    # check if the user is authenticated because if so they'll have a
    # profile that was created when they created their account.
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Save the user's info. The dictionaries keys will match the
        # fields on the user profile model.
        if save_info:
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_country': order.country,
                'default_postcode': order.postcode,
                'default_town_or_city': order.town_or_city,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_county': order.county,
            }
            # create an instance of user profile form, using the profile data
            # we're going to update the profile we've obtained above and if
            # the form is valid just save it.
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()


    # attach success message letting user know what their order number is.
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    # delete the user shopping bag from the session since it'll no longer
    # be needed for this session
    if 'bag' in request.session:
        del request.session['bag']
    # Set the template and the context
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    # and render the template.
    return render(request, template, context)
