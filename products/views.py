from django.shortcuts import render, get_object_or_404
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


def product_detail(request, product_id):
    # a view for returning one product details from the db
    product = get_object_or_404(Product, pk=product_id)

    # add that to the context so our product will be available in template.
    context = {
        'product': product,

    }

    # need a context since we'll need to send some things back to the template
    return render(request, 'products/product_detail.html', context)
  
