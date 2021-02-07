from django.shortcuts import render, redirect


def view_bag(request):
    # A view that renders the bag contents page
    return render(request, 'bag/bag.html')


# We'll submit the form to this view including the product id and the quantity.
# Once in the view we'll get the bag variable if it exists in the
# session or create it if it doesn't. And we'll add the item to the bag
# or update the quantity if it already exists.
def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """
    # Get the quantity form the form, we need to convert it to an integer
    # since it'll come from the template as a string.
    quantity = int(request.POST.get('quantity'))
    # We'll also want to get the redirect URL from the form so we know
    # where to redirect once the process here is finished.
    redirect_url = request.POST.get('redirect_url')
    # every request-response cycle between the server and the client
    # (between the django view on the server-side and our form making
    # the request on the client-side) uses a session, to allow information
    # to be stored until the client and server are done communicating.
    # It allows us to store the contents of the shopping bag in the HTTP
    # session while the user browses the site and adds items to be purchased.
    # create a variable bag which accesses the requests session. Trying to
    # get this variable if it already exists and initializing it to an empty
    # dictionary if it doesn't, so we first check to see if there's a bag
    # variable in the session and if not we'll create one.
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        # I can just stuff the product into dictionary along with the quantity.
        # if there's already a key in bag dictionary matching this product id
        # Then I'll increment its quantity accordingly.
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    request.session['bag'] = bag

    return redirect(redirect_url)
