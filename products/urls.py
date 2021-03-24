from django.urls import path
from . import views

urlpatterns = [
    # empty path to indicate that this is the route URL.
    # And it's going to render views.products. With the name of products.
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),

]
