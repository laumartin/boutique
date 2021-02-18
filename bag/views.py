from django.shortcuts import render, redirect, reverse, HttpResponse


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
    # the shopping bag with information on the sizes of the products in it.
    size = None
    # then if product size is in request.post we'll set it equal to that.
    if 'product_size' in request.POST:
        size = request.POST['product_size']
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

    # if statement to check if a product with sizes is being added.
    if size:
        # If the item is already in the bag check if another item of the same
        # id and same size already exists,if so increment the quantity for
        # that size and otherwise just set it equal to the quantity.
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
            else:
                bag[item_id]['items_by_size'][size] = quantity
        #  If the items not already in the bag we add it as a dictionary
        # with a key of items_by_size.we may have multiple items with this
        # item id but different sizes.
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}

    else:

        if item_id in list(bag.keys()):
            # I can just stuff the product into dictionary along with the quantity.
            # if there's already a key in bag dictionary matching this product id
            # Then I'll increment its quantity accordingly.
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

    request.session['bag'] = bag

    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    # this is coming from a form on the shopping bag page which will contain
    # the new quantity the user wants in the bag,if quantity >0 set the
    # items quantity accordingly,otherwise just remove the item
    if size:
        if quantity > 0:
            # drill into the items by size dictionary, find that specific
            # size and either set its quantity to the updated one or
            # remove it if the quantity submitted is zero.
            bag[item_id]['items_by_size'][size] = quantity
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)

    # If there's no size remove the item entirely by using the pop function.
    else:
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)

    request.session['bag'] = bag
    return redirect(reverse(view_bag))


# allow users to remove items directly without setting quantity to zero.
def remove_from_bag(request, item_id):
    """Remove the items form the shopping bag"""
    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        # if size is in request.post,delete that size key in the items by
        # size dictionary.
        if size:
            del bag[item_id]['items_by_size'][size]
            # if the items by size dictionary is now empty which will
            # evaluate to false,remove the entire item id so we don't
            # end up with an empty items by size dictionary.
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)

        # If there's no size remove the item entirely by using the pop function
        else:
            bag.pop(item_id)

        request.session['bag'] = bag
        # Because this view will be posted to from a JavaScript function.
        # return a 200 HTTP response so the item was successfully removed.
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)
