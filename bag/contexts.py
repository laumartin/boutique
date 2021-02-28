from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

# the function is taking request as a parameter and will return
# a dictionary called context


def bag_contents(request):
    # This is known as a context processor,its purpose is to make
    # this dictionary available to all templates across the entire
    # application, like you can use request.user in any template
    # due to the presence of the built-in request context processor
    # this context concept is same as the context we've used in views
    # difference is we return it directly and make it available to
    # all templates by putting it in settings.py.
    # create an empty list for the bag items to live in.
    # Also total and product count when we start adding things to the bag.
    # initialize those now to zero.
    bag_items = []
    total = 0
    product_count = 0
    # Accessing the shopping bag in the session. Getting it if it already
    # exists. Or initializing it to an empty dictionary if not.
    bag = request.session.get('bag', {})

    # for each item and quantity in bag.items(this is the bag from the session)
    # get the product.Then add its quantity times the price to the total.
    # And then increment the product count by the quantity(item_data).
    # In the case of item with no sizes. The item data will be the quantity
    # in the case of an item that has sizes the sitem data will be a dictionary
    # of all the items by size.
    for item_id, item_data in bag.items():
        # if the item data is an integer then we know the item data is just the
        # quantity.Otherwise we know it's a dictionary we handle it differently
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            # add a dictionary to the list of bag items containing id and
            # quantity,but also the product object itself because that will
            # give access to all the other fields such as the product image etc
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        # Otherwise we know it's a dictionary we need to handle it differently.
        # need to iterate through the inner dictionary of items_by_size
        # incrementing the product count and total accordingly.
        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                # for each of these items,add the size to the bag items
                # returned to the template as well.
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size
                })


    # customers have free delivery if they spend more than the amount
    # specified in the free delivery threshold in settings.py.
    # If it is less than threshold we'll calculate delivery as total
    # multiplied by the standard delivery percentage from settings.py.
    # which in this case is 10%.
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        # let the user know how much more they need to spend to get free
        # delivery by creating a variable
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    # If the total is > or = to the threshold set delivery and
    # free_delivery_delta to zero
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    # add all these items to context so they're available in templates
    # across the site
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total
    }

    return context


