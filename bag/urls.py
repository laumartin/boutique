from django.urls import path
from . import views
urlpatterns = [
    # empty path to indicate that this is the route URL.
    # And it's going to render views.view_bag. With the name of view_bag.
    path('', views.view_bag, name='view_bag')
]