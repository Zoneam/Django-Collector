from dataclasses import fields
from pyexpat import model
from django.forms import ModelForm
from .models import Feeding, Gorilla
from django import forms

class FeedingForm(ModelForm):
    class Meta:
        model = Feeding
        fields = ['date', 'meal']

class GorillaForm(forms.ModelForm):
    class Meta:
        model = Gorilla
        exclude = ['user']