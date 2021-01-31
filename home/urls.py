from django.urls import path
from . import views
urlpatterns = [
    # empty path to indicate that this is the route URL.
    # And it's going to render views.index. With the name of home.
    path('', views.index, name='home')
]
