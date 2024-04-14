from datetime import datetime

from Neo4jConnection import Neo4jConnection

conn = Neo4jConnection()

def find_movies_by_genre(genre, desc=True):
    if desc:
        query = f"""MATCH (n)-[r:WATCHED]->(p:Pelicula)-[r1:PERTENECE_A]->(g:Genero {{nombre: '{genre}'}})
        WITH p AS Peliculas, collect(r.rating) AS RATING
        RETURN Peliculas, reduce(total = 0, n IN RATING | total + n) / size(RATING) AS AVERAGE_RATING
        ORDER BY AVERAGE_RATING DESC"""
    else:
        query = f"""MATCH (n)-[r:WATCHED]->(p:Pelicula)-[r1:PERTENECE_A]->(g:Genero {{nombre: '{genre}'}})
        WITH p AS Peliculas, collect(r.rating) AS RATING
        RETURN Peliculas, reduce(total = 0, n IN RATING | total + n) / size(RATING) AS AVERAGE_RATING
        ORDER BY AVERAGE_RATING ASC"""

    return conn.query(query)