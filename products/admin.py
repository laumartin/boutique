from django.contrib import admin
from .models import Product, Category

# Register your models here.


# product admin and category admin,both will extend built-in model admin class

class ProductAdmin(admin.ModelAdmin):
    # add the list display attribute which is a tuple that will tell
    # the admin which fields to display.
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image'
    )
    # sort the products by SKU using the ordering attribute.Since it's
    # possible to sort on multiple columns note that this does have to
    # be a tuple even though it's only one field.
    # To reverse it you can simply stick a minus in front of SKU
    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name'
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
