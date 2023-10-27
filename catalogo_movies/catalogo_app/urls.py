# catalogo_peliculas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.mostrar_catalogo, name='catalogo'),
]
