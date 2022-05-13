from django.shortcuts import render
from django.http import HttpResponse

import logging
logging.basicConfig(level=logging.DEBUG)


class Gorilla:
    def __init__(self, name, breed, description, age):
        self.name = name
        self.breed = breed
        self.description = description
        self.age = age

gorillas = [
    Gorilla('Abxazzarz', 'Shizi', 'Mountain Gorilla', 11),
    Gorilla('Tivandin', 'Dodoz', 'Cross River Gorilla', 0),
    Gorilla('Rabazanter', 'Alpine Drau', '7 legged gorilla', 5),
    Gorilla('Tixaro', 'Bilduz', 'Gorilla', 12),
    Gorilla('Artsvaqar', 'Entramo', 'Cross River Gorilla', 1),
    Gorilla('Ebaladin', 'Alpine Drau', '1 legged gorilla', 0),
]

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
    return render(request, 'gorillas/index.html', {'gorillas': gorillas})