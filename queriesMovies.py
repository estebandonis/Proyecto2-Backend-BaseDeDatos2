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

    print(query)

    return conn.query(query)


def find_movies_by_director(usuario):
    query = f"""MATCH (n:Usuario {{correo:'{usuario}'}})-[r:LIKED_DIRECTOR]->(d:Director)
    MATCH (p:Pelicula)-[r1:DIRIGIDA_POR]->(d)
    RETURN d,p"""

    print(query)

    return conn.query(query)


def find_movies_by_actor(usuario):

    query = f"""MATCH (n:Usuario {{correo:'{usuario}'}})-[r:LIKED_ACTOR]->(a:Actor)-[r1:ACTUO_EN]->(p:Pelicula)
    RETURN a,p"""

    print(query)

    return conn.query(query)


def add_sequel_to_movie(movie_title, sequel_title, orden, isContinuation):
    query = f"MATCH (p1:Pelicula {{titulo: '{movie_title}'}}) MATCH (p2:Pelicula {{titulo: '{sequel_title}'}}) MERGE (p1)-[r:SECUELA_DE {{diferenciaTiempo: abs(p1.duracion - p2.duracion), orden: {orden}, esContinuacion: {isContinuation}}}]->(p2) RETURN r"
    return conn.query(query)


def find_sequels(movie_title, sequel_title):
    query = f"MATCH (p1:Pelicula {{titulo: '{movie_title}'}})-[r:SECUELA_DE]->(p2:Pelicula {{titulo: '{sequel_title}'}}) RETURN p1,r,p2"
    return conn.query(query)


def upload_csv_peliculas(link):
    query = f"LOAD CSV WITH HEADERS FROM '{link}' AS row MERGE (p:Pelicula {{titulo: row.titulo, duracion: toInteger(row.duracion), clasificacion: row.clasificacion, sinopsis: row.sinopsis, year: toInteger(row.year)}}) RETURN p"

    print(query)

    return conn.query(query)

def upload_csv_relationships(link):
    query = f"LOAD CSV WITH HEADERS FROM '{link}' AS row MATCH (p1:Pelicula {{titulo: row.titulo1}}) MATCH (p2:Pelicula {{titulo: row.titulo2}}) MERGE (p1)-[r:SECUELA_DE {{diferenciaTiempo: toInteger(row.diferenciaTiempo), orden: row.orden, esContinuacion: row.esContinuacion}}]->(p2) RETURN row.titulo1, row.titulo2"

    print(query)

    return conn.query(query)
