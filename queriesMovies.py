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

def add_sequel_to_movie(movie_title, sequel_title, orden, isContinuation):
    query = f"MATCH (p1:Pelicula {{titulo: '{movie_title}'}}) MATCH (p2:Pelicula {{titulo: '{sequel_title}'}}) MERGE (p2)-[r:SECUELA_DE {{diferenciaTiempo: abs(p1.duracion - p2.duracion), orden: {orden}, esContinuacion: {isContinuation}}}]->(p1) RETURN r"
    return conn.query(query)