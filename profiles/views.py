from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm


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