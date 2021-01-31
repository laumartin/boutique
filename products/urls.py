from django.urls import path
from . import views

urlpatterns = [
    # empty path to indicate that this is the route URL.
    # And it's going to render views.products. With the name of products.
    path('', views.all_products, name='products')
]
