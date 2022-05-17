from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseNotFound
from .models import Gorilla
from django.urls import reverse
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
    return render(request, 'gorillas/index.html', { 'gorillas': gorillas })


def gorilla_detail(request, gorilla_id):
    """
    gorillas detail pages
    http://localhost:8000/gorillas/:gorilla_id   
    """
    try:
        gorilla = Gorilla.objects.get(id=gorilla_id)
        return render(request, 'gorillas/detail.html', { 'gorilla': gorilla })
    except Gorilla.DoesNotExist:
        return HttpResponseNotFound("<h1 style='text-align: center; margin-top: 200px;'>ERROR <span style='color: red; font-size:70px'>404</span> PAGE NOT FOUND !</h1>")
    
    
class GorillaCreate(CreateView):
    model = Gorilla
    fields = '__all__'
    # success_url = '/gorillas/'
    
    def get_success_url(self, **kwargs):
        return reverse('detail', args=(self.object.id,))
    
class GorillaUpdate(UpdateView):
    model = Gorilla
    fields = ['description', 'age']
    success_url = '/gorillas/'
    
class GorillaDelete(DeleteView):
    model = Gorilla
    success_url = '/gorillas/'