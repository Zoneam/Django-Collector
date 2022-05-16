from django.shortcuts import render
from django.http import HttpResponse
from .models import Gorilla
import logging
logging.basicConfig(level=logging.DEBUG)


def home(request):
    """
    home view
    http://localhost:8000/
    """
    return HttpResponse("Hello World")


def about(request):
    """
    about view
    http://localhost:8000/about
    """
    # if you have a folder inside the template dir
    # then you should use the following syntax
    # return render(request, 'folder_name/about.html')
    return render(request, 'about.html')


def gorillas_index(request):
    """
    gorillas index pages
    http://localhost:8000/gorillas/   
    """
    logging.info('calling gorillas_index')
    # context means : a dictionary of values to add to the template
    # context must have two values {'key': 'value'}
    # key we can use inside the template
    gorillas = Gorilla.objects.all()
    return render(request, 'gorillas/index.html', {'gorillas': gorillas})


def gorilla_detail(request, gorilla_id):
    """
    gorillas detail pages
    http://localhost:8000/gorillas/:gorilla_id   
    """
    gorilla = Gorilla.objects.get(id=gorilla_id)
    return render(request, 'gorillas/detail.html', {'gorilla': gorilla})