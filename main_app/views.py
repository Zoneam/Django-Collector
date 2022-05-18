from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Gorilla, Toy
from .forms import FeedingForm
from django.http import HttpResponseNotFound


# View functions


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def gorillas_index(request):
    gorillas = Gorilla.objects.all()
    return render(request, 'gorillas/index.html', {'gorillas': gorillas})


def gorilla_detail(request, gorilla_id):
    try:
        gorilla = Gorilla.objects.get(id=gorilla_id)
        toys_gorilla_doesnt_have = Toy.objects.exclude(id__in = gorilla.toys.all().values_list('id'))
        feeding_form = FeedingForm()
        return render(request, 'gorillas/detail.html', {'gorilla': gorilla, 'feeding_form': FeedingForm, 'toys': toys_gorilla_doesnt_have,})
    except Gorilla.DoesNotExist:
        # return HttpResponseNotFound("<h1 style='text-align: center; margin-top: 200px;'>ERROR <span style='color: red; font-size:70px'>404</span> PAGE NOT FOUND !</h1><h2 style='text-align: center;'>No Gorillas Here Sorry !!!</h2>")
        return render(request, 'notfound.html')

def add_feeding(request, gorilla_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.gorilla_id = gorilla_id
        new_feeding.save()
    return redirect('detail', gorilla_id = gorilla_id)

def assoc_toy(request, gorilla_id, toy_id):
    Gorilla.objects.get(id = gorilla_id).toys.add(toy_id)
    return redirect('detail', gorilla_id = gorilla_id)


class GorillaCreate(CreateView):
    model = Gorilla
    fields = '__all__'
    success_url = '/gorillas/'


class GorillaUpdate(UpdateView):
    model = Gorilla
    # Let's disallow the renaming of a gorilla by excluding the name field!
    fields = ['breed', 'description', 'age']


class GorillaDelete(DeleteView):
    model = Gorilla
    success_url = '/gorillas/'

