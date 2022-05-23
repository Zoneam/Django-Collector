import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Gorilla, Toy, Photo
from .forms import FeedingForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):
    return render(request, 'home.html')


@login_required
def about(request):
    return render(request, 'about.html')


@login_required
def gorillas_index(request):
    gorillas = Gorilla.objects.filter(user=request.user)
    return render(request, 'gorillas/index.html', {'gorillas': gorillas})


@login_required
def gorilla_detail(request, gorilla_id):
    try:
        gorilla = Gorilla.objects.get(id=gorilla_id)
        toys_gorilla_doesnt_have = Toy.objects.exclude(id__in = gorilla.toys.all().values_list('id'))
        feeding_form = FeedingForm()
        return render(request, 'gorillas/detail.html', {'gorilla': gorilla, 'feeding_form': FeedingForm, 'toys': toys_gorilla_doesnt_have,})
    except Gorilla.DoesNotExist:
        return render(request, 'notfound.html')


def signup(request):
    error_message = ''
    if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
      # This will add the user to the database
            user = form.save()
      # This is how we log a user in via code
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


@login_required
def add_feeding(request, gorilla_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.gorilla_id = gorilla_id
        new_feeding.save()
    return redirect('detail', gorilla_id = gorilla_id)


@login_required
def assoc_toy(request, gorilla_id, toy_id):
    Gorilla.objects.get(id = gorilla_id).toys.add(toy_id)
    return redirect('detail', gorilla_id = gorilla_id)

def unassoc_toy(request, gorilla_id, toy_id):
    Gorilla.objects.get(id=gorilla_id).toys.remove(toy_id)
    return redirect('detail', gorilla_id=gorilla_id)


@login_required
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


class GorillaCreate(LoginRequiredMixin, CreateView):
    model = Gorilla
    fields = '__all__'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class GorillaUpdate(LoginRequiredMixin, UpdateView):
    model = Gorilla
    # Let's disallow the renaming of a gorilla by excluding the name field!
    fields = ['breed', 'description', 'age']
    success_url = '/gorillas/'


class GorillaDelete(LoginRequiredMixin, DeleteView):
    model = Gorilla
    success_url = '/gorillas/'
    
class ToyList(LoginRequiredMixin, ListView):
      model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy

class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys/'
