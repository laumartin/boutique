from django.shortcuts import render
from .models import Product
# Create your views here.


def all_products(request):
    # returning all products from the db
    products = Product.objects.all()

    # add that to the context so our products will be available in template.
    context = {
        'products': products,

    }

    # A view to show all products, including sorting and search queries
    # need a context since we'll need to send some things back to the template
    return render(request, 'products/products.html', context)


  
