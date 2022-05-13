from os import abort
from django.urls import path
# from the current dir .
# import the view file
from . import views

urlpatterns = [
    # http://localhost:8000
    path('', views.home, name="home"),

    # http://localhost:8000/about/
    path('about/', views.about, name="about"),

    # http://localhost:8000/gorillas/
    path('gorillas/', views.gorillas_index, name='index')
]