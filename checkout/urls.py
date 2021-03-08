from django.urls import path
from . import views
from .webhooks import webhook


urlpatterns = [
    # empty path to indicate that this is the route URL.
    # And it's going to render views.index. With the name of home.
    path('', views.checkout, name='checkout'),
    path('checkout_success/<order_number>', views.checkout_success, name='checkout_success'),
    path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),
    path('wh/', webhook, name='webhook'),
]