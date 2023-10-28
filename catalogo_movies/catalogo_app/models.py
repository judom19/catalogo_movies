from django.db import models
from django.db.models import ImageField

# modelo para almacenar las categorias provenitentes desde la API
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

# modelo para almacenar las peliculas provenitentes desde la API
class Pelicula(models.Model):
    titulo = models.CharField(max_length=200)
    categorias = models.ManyToManyField(Categoria)
    sinopsis = models.TextField(blank=True, null=True,default='')
    imagen = ImageField(upload_to='imagenes/portadas/', null=True, blank=True, default='imagen_portada')
    def __str__(self):
        return self.titulo
    
# modelo para almacenar las series provenitentes desde la API
class Serie(models.Model):
    id = models.IntegerField(primary_key=True)
    titulo_serie = models.CharField(max_length=255)
    imagen_serie = models.URLField(default=None, blank=True, null=True)
    sinopsis_serie = models.TextField(blank=True, null=True,default='')
    
    def __str__(self):
        return self.titulo_serie