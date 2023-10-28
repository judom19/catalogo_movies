# se importa el modulo requests para hacer las peticiones HTTP
import requests
# se importan los modelos Pelicula y Categoria desde models.py
from .models import Pelicula, Categoria, Serie
# se importa a la llave de la cuenta 'TMDB_API_KEY' desde el archivo secret.py
from .secret import TMDB_API_KEY
# se importa la funcion render de Django para renderizar la plantilla HTML
from django.shortcuts import render

# funcion encargada de obtener la informacion de las peliculas de la API de The Movie Database (TMDB)
def obtener_informacion_peliculas():
    
    # se inicia una peticion HTTP al endpoint /genre/movie/list de TMDB para obtener la lista de generos
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
                
                # se asigan las imagenes por medio del campo 'poster_path' desde la data local
                pelicula.imagen = f"https://image.tmdb.org/t/p/w500/{pelicula_data['poster_path']}"
                
                #se asignan la sinopsis perteneciante a cada pelicula desde el campo 'overview' obtenido desde la data local y se asigna al campo 'sinopsis'
                pelicula.sinopsis = pelicula_data['overview']
                
                #se guarda la pelicula
                pelicula.save()
        
        # se devuelve la pelicula
        return pelicula
    

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



# funcion para obtener las serias desde la API 
def obtener_series():
    
    # se eliminan todas las series existentes en la base de datos para no duplicar cada que carga la vista
    Serie.objects.all().delete()

    # se inicia la petición HTTP al endpoint para obtener las series desde la API
    series_url = f"http://api.themoviedb.org/3/tv/popular?api_key={TMDB_API_KEY}" # se construye la URL

    # se realiza la petición GET a la URL en 'series_url'
    series_response = requests.get(series_url)

    # si la petición es correcta, se devuelve el objeto JSON con los datos de las series
    if series_response.status_code == 200:

        # se parsean los datos de formato JSON a estructura de datos en Python
        series_data = series_response.json()

        # se crea la lista de series por medio de la clase 'results' del objeto JSON recibido desde la API y se almacena en la variable 'series'
        series = series_data.get("results", [])

        # se almacenan los datos usando los campos provenientes de la API y asignándolos a los campos del modelo local
        for series_data in series:
            serie = Serie(
                titulo_serie=series_data["name"],
                imagen_serie=f"https://image.tmdb.org/t/p/w500{series_data['poster_path']}",
                sinopsis_serie=series_data["overview"],
            )

            # se guarda la instancia del objeto serie
            serie.save()

        # se devuelven las series
        return series   


# vista encargada de mostrar todas las categorías y las películas que pertenecen a esas categorías
def mostrar_categorias(request):
    
    # varible para validacion de vista
    en_categorias = True
    
    # verifica si los datos ya existen en la base de datos local
    if Categoria.objects.exists() and Pelicula.objects.exists():
        
        # si existen, se obtienen las categorias y peliculas existentes, esto evita la duplicidad de los datos
        categorias = Categoria.objects.all()
    else:
        # si no existen, se llama a la funcion que obtiene la informacioj de las peliculas desde la API
        obtener_informacion_peliculas()
        
        # se obtienen todas las categorias
        categorias = Categoria.objects.all()

    # se crea una lista de diccionarios para almacenar las categorias y las peliculas que pertenecen a cada categoria
    categorias_y_peliculas = []
    
    for categoria in categorias:
        # se obtienen todas las peliculas que pertenecen a la categoria actual
        peliculas = Pelicula.objects.filter(categorias=categoria)

        # se agrega la categoria y las peliculas a la lista
        categorias_y_peliculas.append({
            'categoria': categoria,
            'peliculas': peliculas,
        })

    # se pasan las categorias y peliculas al template por contexto
    context = {
        'categorias_y_peliculas': categorias_y_peliculas,
        'en_categorias':en_categorias,
        
    }

    # se renderiza el template que mostrará la lista de categorías y las películas que pertenecen a ellas
    return render(request, 'catalogo_movies/categorias.html', context)





#vista encargada de mostar las series    
def mostrar_series(request):
    
    # se llama la funcion que obtiene las series desde la API   
    obtener_series()
    # se obtienen todas las series de la base de datos
    series = Serie.objects.all()
    
    # se pasan por contexto al template
    context = {
        'series': series,
    }
    
    # se renderiza el template que mostrara las lista de series 
    return render(request, 'catalogo_movies/series.html', context)
    
    

