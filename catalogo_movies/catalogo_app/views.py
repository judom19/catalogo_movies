from django.shortcuts import render
from .models import Pelicula, Categoria

def catalogo(request):
    peliculas = Pelicula.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'catalogo_peliculas/catalogo.html', {'peliculas': peliculas, 'categorias' : categorias})

