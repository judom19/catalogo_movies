from django.contrib import admin
from .models import Categoria, Pelicula, Serie

# mostrando los modelos en el admin
admin.site.register(Categoria)
admin.site.register(Pelicula)
admin.site.register(Serie)
