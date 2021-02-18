from django import template

# to register this filter we need to create a variable called register.
# Which is an instance of template.library
register = template.Library()


# use the register filter decorator to register function as a
# template filter. All of this is from the django documentation
# for creating custom template tags and filters.
@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    return price * quantity
