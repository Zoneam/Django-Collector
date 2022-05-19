import boto3
import uuid, os
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Gorilla, Toy, Photo
from .forms import FeedingForm
from django.views.generic import ListView, DetailView
from django.http import HttpResponseNotFound


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

def unassoc_toy(request, gorilla_id, toy_id):
    Gorilla.objects.get(id=gorilla_id).toys.remove(toy_id)
    return redirect('detail', gorilla_id=gorilla_id)

def add_photo(request, gorilla_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to gorilla_id or gorilla (if you have a gorilla object)
            Photo.objects.create(url=url, gorilla_id=gorilla_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', gorilla_id=gorilla_id)


class GorillaCreate(CreateView):
    model = Gorilla
    fields = '__all__'
    success_url = '/gorillas/'


class GorillaUpdate(UpdateView):
    model = Gorilla
    # Let's disallow the renaming of a gorilla by excluding the name field!
    fields = ['breed', 'description', 'age']
    success_url = '/gorillas/'


class GorillaDelete(DeleteView):
    model = Gorilla
    success_url = '/gorillas/'
    
class ToyList(ListView):
      model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'
