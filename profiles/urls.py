from django.urls import path
from . import views
urlpatterns = [
    # empty path to indicate that this is the route URL.
    # And it's going to render views.index. With the name of home.
    path('', views.profile, name='profile'),
    path('order_history/<order_number>', views.order_history, name='order_history'),
]
