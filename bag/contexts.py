from decimal import Decimal
from django.conf import settings
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


