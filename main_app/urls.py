from django.urls import path, include
from . import views
from django.contrib import admin

# from the current dir .
from django.urls import reverse

urlpatterns = [
    # http://localhost:8000
    path('', views.home, name="home"),

    # http://localhost:8000/about/
    path('about/', views.about, name="about"),

    # http://localhost:8000/gorillas/
    path('gorillas/', views.gorillas_index, name='index'),

    # http://localhost:8000/gorillas/:gorillas_id
    # _id is integer
    path('gorillas/<int:gorilla_id>', views.gorilla_detail, name='detail'),
    path('gorillas/create/', views.GorillaCreate.as_view(), name='gorillas_create'),
    path('gorillas/<int:pk>/update/', views.GorillaUpdate.as_view(), name='gorillas_update'),
    path('gorillas/<int:pk>/delete', views.GorillaDelete.as_view(), name='gorillas_delete'),
    path('gorillas/<int:gorilla_id>/add_feeding/', views.add_feeding, name='add_feeding'),
    path('gorillas/<int:gorilla_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'),
]
