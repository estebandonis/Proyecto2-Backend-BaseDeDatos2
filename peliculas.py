from flask import Blueprint, request, jsonify
from flask_restful import Resource, reqparse
from neo4j import GraphDatabase, RoutingControl
from flask import request, jsonify
from flask_cors import CORS, cross_origin
import json

import queries
import queriesMovies

api = Blueprint('peliculas', __name__)
cors = CORS(api)

@api.route('/', methods=['GET'])
def home():
    return "Aqui se encuentran las peliculas"

@api.route('/info', methods=['GET'])
def info():
    results = queries.find_node(["Pelicula"], [("titulo","A unbreakable legend")])
    movies = []
    for result in results:
        new_result = result['n']

        # Extract properties
        properties = dict(new_result)
        movies.append(properties)

    return movies

@api.route('/getMovieTitulo', methods=['POST'])
def getMovie():
    data = request.get_json()
    results = queries.find_node(["Pelicula"], [("titulo", data['titulo'])])
    movies = []
    for result in results:
        new_result = result['n']

        # Extract properties
        properties = dict(new_result)
        movies.append(properties)

    return movies


@api.route('/getMovieGenero', methods=['POST'])
def getMovieGenero():
    data = request.get_json()
    results = queriesMovies.find_movies_by_genre(data['genero'], data['desc'])
    movies = []
    for result in results:
        new_result = result['Peliculas']
        avg = result['AVERAGE_RATING']
        genero = data['genero']

        # Extract properties
        properties = dict(new_result)
        properties['averRating'] = avg
        properties['genero'] = genero
        movies.append(properties)

    return movies


@api.route('/getMovieDirector', methods=['POST'])
def getMovieDirector():
    data = request.get_json()
    results = queriesMovies.find_movies_by_director(data['user'])
    movies = []
    for result in results:
        new_result = result['d']

        properties = dict(new_result)
        date = properties['yearBorn']
        python_date = date.to_native()
        js_date_string = python_date.strftime('%Y-%m-%d')
        properties['yearBorn'] = js_date_string
        directorName = ""
        directorLastName = ""
        if properties not in movies:
            directorName = properties['nombre']
            directorLastName = properties['apellido']

        new_result = result['p']

        # Extract properties
        properties = dict(new_result)
        properties['nombre'] = directorName
        properties['apellido'] = directorLastName
        if properties not in movies:
            movies.append(properties)

    return movies


@api.route('/getMovieActor', methods=['POST'])
def getMovieActor():
    data = request.get_json()
    results = queriesMovies.find_movies_by_actor(data['user'])
    movies = []
    for result in results:
        new_result = result['a']

        properties = dict(new_result)
        date = properties['yearBorn']
        python_date = date.to_native()
        js_date_string = python_date.strftime('%Y-%m-%d')
        properties['yearBorn'] = js_date_string
        directorName = ""
        directorLastName = ""
        if properties not in movies:
            directorName = properties['nombre']
            directorLastName = properties['apellido']

        new_result = result['p']

        # Extract properties
        properties = dict(new_result)
        properties['nombre'] = directorName
        properties['apellido'] = directorLastName
        if properties not in movies:
            movies.append(properties)

    return movies


@api.route('/setMovieSequel', methods=['POST'])
def setMovieSequel():
    data = request.get_json()
    results = queriesMovies.add_sequel_to_movie(data['first'], data['second'], data['orden'], data['isContinuation'])
    if results == []:
        return "false"
    else:
        return "true"


@api.route('/getMovieSequel', methods=['POST'])
def getMovieSequel():
    data = request.get_json()
    results = queriesMovies.find_sequels(data['first'], data['second'])
    resultado = []
    for result in results:
        new_result = result['p1']
        properties = dict(new_result)
        resultado.append(properties)

        new_result = result['p2']
        properties = dict(new_result)
        resultado.append(properties)

        new_result = result['r']
        properties = dict(new_result)
        resultado.append(properties)

    return resultado

@api.route('/upload_csv_nodes', methods=['POST'])
def upload_csv_nodes():
    data = request.get_json()

    results = queriesMovies.upload_csv_peliculas(data['link'])

    return "false" if results == [] else "true"


@api.route('/upload_csv_relaciones', methods=['POST'])
def upload_csv_relaciones():
    data = request.get_json()

    results = queriesMovies.upload_csv_relationships(data['link'])

    return results


# @api.route('/create_node', methods=['POST'])
# def create_node():
#     data = request.get_json()

#     # Your API logic here
#     node_type = data.get('type', 'Node')  # Get the node type from the data, default to 'Node'
#     node_properties = data.get('properties', {})  # Get the node properties from the data

#     # Create the node
#     query = f"MERGE (n:{node_type} {{ title: '{node_properties.get('title')}', tagline: '{node_properties.get('tagline')}', released: {int(node_properties.get('released'))}}}) RETURN n"

#     result = conn.query(query)

#     return "Movie added!"

# @api.route('/create_relation_SECUELADE', methods=['POST'])
# def create_relation_SECUELADE():
#     data = request.get_json()

#     # Your API logic here
#     start_node = data.get('start_node', {})
#     end_node = data.get('end_node', {})
#     relation_type = data.get('relation_type', 'SECUELA_DE')

#     # Create the relation
#     query = f"MERGE (m1:Movie {{title: '{start_node}'}}) MERGE (m2:Movie {{title: '{end_node}'}}) MERGE (m1)-[r:{relation_type}]->(m2) RETURN r"

#     result = conn.query(query)

#     return "Relation added!"
