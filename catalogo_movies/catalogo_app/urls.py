# catalogo_peliculas/urls.py
from django.urls import path
from . import views

# identificador de nombre de urls de la app
app_name = 'catalogo_app'

urlpatterns = [
    path('', views.mostrar_catalogo, name='catalogo'),
    path('categorias', views.mostrar_categorias, name='categorias'),
    path('series', views.mostrar_series, name='series'),
]
