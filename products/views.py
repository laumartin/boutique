from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
# If the query isn't blank,use a special object from Jango.db.models
# called Q to generate a search query.
from django.db.models import Q
# we should grab those categories anyway so we can display for the user
# which categories they currently have selected.For that,import category
from .models import Product, Category
# Create your views here.


def all_products(request):
    # returning all products from the db
    products = Product.objects.all()
    # set none to not get error when loading products page without search term.
    query = None
    categories = None
    # when we submit a search query It'll end up in the url as a get parameter.
    # We can access those url parameters in the all_products view by checking
    # whether request.get exists. Since we named the text input in the form q.
    # We can just check if q is in request.get If it is I'll set it equal to
    # a variable called query.
    if request.GET:
        # if category exists in requests.get split it into a list at the commas
        # then use that list to filter the current query set of all products
        # down to only products whose category name is in the list.
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            # this __ means we look for the name field of the category model,we
            # can because category and product are related with a foreign key
            products = products.filter(category__name__in=categories)
            # Filter all categories down to the ones whose name is in the list
            # from the URL,we're converting the list of strings of category
            # names passed through the URL into a list of actual category
            # objects,to access all their fields in template.
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            # If the query is blank use Django messages framework to attach
            # an error message to the request and redirect back to products url
            # We'll also need to import messages, redirect, and reverse
            if not query:
                messages.error(request, "You didn't enter any search criteria")
                return redirect(reverse('products'))
            # Set a variable = Q object. Where the name contains the query or
            # description contains the query, i makes queries case insensitive
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            # pass them to the filter method to actually filter the products.
            products = products.filter(queries)

    # add that to the context so our products will be available in template.
    context = {
        'products': products,
        # add the query to the context and in the template call it search term.
        'search_term': query,
        # call that list of category objects, current_categories, and return
        # it to the context so we can use it in the template later on.
        'current_categories': categories,
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
  
