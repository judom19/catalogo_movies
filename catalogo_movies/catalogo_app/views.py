# se importa el modulo requests para hacer las peticiones HTTP
import requests
# se importan los modelos Pelicula y Categoria desde models.py
from .models import Pelicula, Categoria
# se importa a la llave de la cuenta 'TMDB_API_KEY' desde el archivo secret.py
from .secret import TMDB_API_KEY
# se importa la funcion render de Django para renderizar la plantilla HTML
from django.shortcuts import render

# funcion encargada de obtener la informacion de las peliculas de la API de The Movie Database (TMDB)
def obtener_informacion_peliculas():
    
    #primero se inicia una peticion HTTP al endpoint /genre/movie/list de TMDB para obtener la lista de generos
    generos_url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}" # se construye la URL a utilizar para la peticion
    generos_response = requests.get(generos_url) # se realiza la solicitud GET a la URL en 'generos_url'
    
    # si la peticion es correcta, la funcion devuelve el objeto JSON con los datos de los generos de peliculas
    if generos_response.status_code == 200:
        generos_data = generos_response.json() # parseando los datos recibidos en formato JSON a datos estructurados en Python
        
        # despues de parsear los datos se crea un diccionario mapeando los ID de los generos con sus nombres de generos utilizando compresion de diccionarios
        mapeo_generos = {genero['id']: genero['name'] for genero in generos_data['genres']}
        
        # ahora se inicia una peticion HTTP al endpoint /discover/movie de TMDB para obtener la lista de las peliculas desde la API
        peliculas_url =f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}" # se construye la URL a utilizar para la peticion
        peliculas_response = requests.get(peliculas_url) # se realiza la solicitud GET a la URL en 'peliculas_url'
        
        # si la peticion es correcta, la funcion devuelve el objeto JSON con los datos de los generos de peliculas
        if peliculas_response.status_code == 200:
            
            data = peliculas_response.json()# parseando los datos recibidos en formato JSON a datos estructurados en Python
            
            # se crea la lista de peliculas por medio de la clave 'results' del objeto JSON recibido desde la API y se almacena en la variable 'pelicula'
            películas = data.get("results", [])
            
            # para cada pelicula, se obtiene la lista de ID de los generos a los que pertenece por medio de la clave 'genre_ids'
            for pelicula_data in películas:
                categorias_ids = pelicula_data.get("genre_ids", [])                
                # ahora se crea un lista con los nombres de los generos a los que pertenece la pelicula
                categorias_nombres = [mapeo_generos[genero_id] for genero_id in categorias_ids]
                
                # se busca la pelicula en la base de datos obteniendo el titulo de la pelicula por medio de la clave 'title'
                pelicula, _ = Pelicula.objects.get_or_create(titulo=pelicula_data['title'])
                
                # se itera sobre la lista de ID de los generos a los que pertenece la pelicula
                for categoria_id, categoria_nombre in zip(categorias_ids, categorias_nombres):                    
                    # se busca el genero en la base de datos
                    categoria, _ = Categoria.objects.get_or_create(id = categoria_id, nombre=categoria_nombre)
                    # se asocia la pelicula a sus generos/categorias
                    pelicula.categorias.add(categoria)
                    
                # se actualiza la lista de categorias de la pelicula, que se obtiene de la API y se almacena en el modelo local
                # 'categorías' hace referencia a las categorias de la pelicula desde la API y 'categorias' hace referencia a las categorias de modelo local
                pelicula.categorías = pelicula.categorias.all()
                

# funcion encargada de mostrar el catalogo de peliculas
def mostrar_catalogo(request):
    # se llama la funcion obtener_informacion_peliculas() para obtener la informacion de las peliculas
    obtener_informacion_peliculas()
    
    # se obtiene la lista de peliculas de la base de datos
    peliculas = Pelicula.objects.all()
    
    # se obtienen las categorias de la base de datos
    categorias = Categoria.objects.all()
    
    # se define el contexto que se le pasara a la platntilla a renderizar la informacion
    context = {
        'peliculas': peliculas,
        'categorias': categorias,
    }
    
    # y se devuele la plantilla a rederizar pasando le informacion por medio del contexto
    return render(request, 'catalogo_movies/catalogo.html', context)

