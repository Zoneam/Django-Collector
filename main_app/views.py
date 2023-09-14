import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Gorilla, Toy, Photo
from .forms import FeedingForm, GorillaForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseServerError


def home(request):
    try:
        return render(request, 'home.html')
    except Exception as e:
        # Log the exception for debugging purposes (optional)
        # logging.error(f"Error rendering home page: {e}")
        return HttpResponseServerError("There was an error displaying the Home page. Please try again later.")


@login_required
def about(request):
    try:
        return render(request, 'about.html')
    except Exception as e:
        # Log the exception for debugging purposes (optional)
        # logging.error(f"Error rendering about page: {e}")
        return HttpResponseServerError("There was an error displaying the About page. Please try again later.")


@login_required
def gorillas_index(request):
    try:
        gorillas = Gorilla.objects.filter(user=request.user)
        return render(request, 'gorillas/index.html', {'gorillas': gorillas})
    except Exception as e:
        # catch-all for unexpected errors.
        return HttpResponseServerError("There was an error fetching the data. Please try again later.")


@login_required
def gorilla_detail(request, gorilla_id):
    try:
        gorilla = Gorilla.objects.get(id=gorilla_id)
        toys_gorilla_doesnt_have = Toy.objects.exclude(id__in=gorilla.toys.all().values_list('id'))
        feeding_form = FeedingForm()
        return render(request, 'gorillas/detail.html', {'gorilla': gorilla, 'feeding_form': feeding_form, 'toys': toys_gorilla_doesnt_have})
    
    except Gorilla.DoesNotExist:
        return render(request, 'notfound.html')
    
    except Exception as e:
        # Handle other unexpected errors
        # Consider logging the exception for debugging in production settings
        return render(request, 'error.html', {'error_message': "Something went wrong. Please try again later."})


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

@login_required
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
    form_class = GorillaForm
    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            return super().form_valid(form)
        except Exception as e:
            # catch-all for unexpected errors
            return HttpResponseServerError("There was an error creating the Gorilla. Please try again later.")


class GorillaUpdate(LoginRequiredMixin, UpdateView):
    model = Gorilla
    # Let's disallow the renaming of a gorilla by excluding the name field!
    fields = ['breed', 'description', 'age']
    success_url = '/gorillas/'

    def get_queryset(self):
        # Ensure users can only update gorillas they own
        return Gorilla.objects.filter(user=self.request.user)

    def form_valid(self, form):
        try:
            # Trying to save the gorilla instance
            return super().form_valid(form)
        except Exception as e:
            # Catch any unexpected errors during save
            return HttpResponseServerError("There was an error updating the Gorilla. Please try again later.")

    def form_invalid(self, form):
        # additional handling form validation fails
        return super().form_invalid(form)

class GorillaDelete(LoginRequiredMixin, DeleteView):
    model = Gorilla
    success_url = '/gorillas/'

    def get_queryset(self):
        # Ensure users can only delete gorillas they own
        return Gorilla.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        try:
            # Try deleting the gorilla instance
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            # Catch any unexpected errors during delete
            return HttpResponseServerError("There was an error deleting the Gorilla. Please try again later.")
    
class ToyList(LoginRequiredMixin, ListView):
    model = Toy

    def get_queryset(self):
        try:
            # Try to get all Toy objects
            return Toy.objects.all()
        except Exception as e:
            # Catch any unexpected errors during the query
            # In a production setting, consider logging the exception for debugging
            self.template_name = "error_template.html"  # we can set this to a specific error template
            return Toy.objects.none()  # Return an empty queryset

    def get(self, request, *args, **kwargs):
        try:
            # Let the ListView handle the GET request as usual
            return super().get(request, *args, **kwargs)
        except Exception as e:
            # Catch any other unexpected errors
            # In a production setting, consider logging the exception for debugging
            return HttpResponseServerError("There was an error fetching the list of toys. Please try again later.")

class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy

    def get_object(self, queryset=None):
        try:
            # Let the DetailView retrieve the object as usual
            return super().get_object(queryset)
        except Toy.DoesNotExist:
            # Handle the case where the Toy instance doesn't exist
            self.template_name = "toy_not_found.html"  # Set to a specific "not found" template
            return None
        except Exception as e:
            # Catch any other unexpected errors
            # In a production setting, consider logging the exception for debugging
            self.template_name = "error_template.html"
            return None

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if not self.object:
            return HttpResponseServerError("There was an error fetching the toy details. Please try again later.")
        return response


class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'

    def form_valid(self, form):
        try:
            # Try saving the Toy instance
            return super().form_valid(form)
        except Exception as e:
            # Catch any unexpected errors during save
            # In a production setting, consider logging the exception for debugging
            form.add_error(None, "There was an error creating the Toy. Please try again later.")
            return self.form_invalid(form)

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color']

    def form_valid(self, form):
        try:
            # Try saving the updated Toy instance
            return super().form_valid(form)
        except Exception as e:
            # Catch any unexpected errors during update
            # In a production setting, consider logging the exception for debugging
            form.add_error(None, "There was an error updating the Toy. Please try again later.")
            return self.form_invalid(form)

class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'

    def delete(self, request, *args, **kwargs):
        try:
            # Try deleting the Toy instance
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            # Catch any unexpected errors during delete
            # In a production setting, consider logging the exception for debugging
            return HttpResponseServerError("There was an error deleting the Toy. Please try again later.")
