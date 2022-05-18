from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Gorilla, Toy
from .forms import FeedingForm

# View functions


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def gorillas_index(request):
    gorillas = Gorilla.objects.all()
    return render(request, 'gorillas/index.html', {'gorillas': gorillas})


def gorilla_detail(request, gorilla_id):
    gorilla = Gorilla.objects.get(id=gorilla_id)
    # print("calling gorillas_detail ==========+>")
    # print(dir(gorilla))
    toys_gorilla_doesnt_have = Toy.objects.exclude(id__in = gorilla.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'gorillas/detail.html', {'gorilla': gorilla, 'feeding_form': FeedingForm, 'toys': toys_gorilla_doesnt_have,})


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
    fields = ['name', 'breed', 'description', 'age']
    success_url = '/gorillas/'


class GorillaUpdate(UpdateView):
    model = Gorilla
    # Let's disallow the renaming of a gorilla by excluding the name field!
    fields = ['breed', 'description', 'age']


class GorillaDelete(DeleteView):
    model = Gorilla
    success_url = '/gorillas/'

