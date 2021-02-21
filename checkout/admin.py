from django.contrib import admin
from .models import Order, OrderLineItem


# inline item allow to add and edit line items in the admin right from
# inside the order model.So when we look at an order see a list of editable
# line items on the same page.
class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)
    fk_name = 'order'


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)
    fk_name = 'order'
    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total',)

# fields option allows to specify the order of the fields in admin interface
# this way order stays same as it appears in the model
    fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total',)

# use the list display option to restrict the columns that show up in the
# order list to only a few key items.
    list_display = ('order_number', 'date', 'full_name', 'order_total',
                    'delivery_cost', 'grand_total',)
    # set them to be ordered by date in reverse chronological order
    # putting the most recent orders at the top.
    ordering = ('-date',)


# register the Order model and the OrderAdmin.skip registering the
# OrderLineItem model since it's accessible via the inline on the order model.
admin.site.register(Order, OrderAdmin)
