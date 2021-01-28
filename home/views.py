from django.shortcuts import render

# Create your views here.


def index(request):
    # this index view will simply render the index template
    return render(request, 'home/index.html')
