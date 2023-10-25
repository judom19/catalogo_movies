import requests
from .models import Pelicula, Categoria
from .secret import TMDB_API_KEY

#vista encargada de obtener la informacion de las peliculas de la API de TMDb
def obtener_informacion_peliculas_api():    
    #se contruye la url para hacer una solicitud a la API de TMBb
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}"
    
    #se realiza una solicitud GET a la url
    response = requests.get(url)
    
    #si la solicitud se completa con exito (codigo de estado 200)
    if response.status_code==200:        
        #se obtienen los datos de la respuesta en formato JSON
        data = response.json()
        
        #se extrae la lista de peliculas de la respuesta
        peliculas = data.get("results", [])
        
        #se itera sobre la lista de peliculas obtenidas de la API
        for pelicula_data in peliculas:            
            #se extraen las categorias de la pelicula con genre_ids
            categorias = pelicula_data.get("genre_ids", [])
            
            #se crea una instancia de la pelicula en la base de datos local usando el titulo de la pelicula
            pelicula, created = Pelicula.objects.get_or_create(
                titulo=pelicula_data['title'],
                
                )
            
            #se agregan las categorias a la pelicula
            for categoria_id  in categorias:
                #se busca o crea un instancia de lka clase Categoria en la base de datos segun el ID de categoria
                categoria, _ = Categoria.objects.get_or_create(id=categoria_id)
                
                #se agrega la categoria a la pelicula
                pelicula.categorias.add(categoria)
    else:
        return None
    
def catalogo