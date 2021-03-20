from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import Order


def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)
# post handler for the profile view.if the request method is post.
# Create a new instance of the user profile form using post data.
# tell it the instance we're updating is the profile we've just
# retrieved above.
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
    # if the form is valid,save it and add a success message.
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')

    form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))
    # use the checkout success template since that template already has
    # layout for rendering order confirmation so we don't have to redo.
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        # added variable from_profile to check in that template if
        # the user got there via the order history view.
        'from_profile': True,
    }

    return render(request, template, context)
