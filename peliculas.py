from flask import Blueprint, request, jsonify
from flask_restful import Resource, reqparse
from neo4j import GraphDatabase, RoutingControl
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from Neo4jConnection import Neo4jConnection

import json

api = Blueprint('peliculas', __name__)
cors = CORS(api)

conn = Neo4jConnection()

@api.route('/', methods=['GET'])
def home():
    return "Aqui se encuentran las peliculas"

@api.route('/info', methods=['GET'])
def info():
    results = conn.query("MATCH (p:Pelicula) RETURN p LIMIT 5")
    movies = []
    for result in results:
        new_result = result['p']

        # Extract properties
        properties = dict(new_result)
        movies.append(properties)

    return movies

@api.route('/create_node', methods=['POST'])
def create_node():
    data = request.get_json()

    # Your API logic here
    node_type = data.get('type', 'Node')  # Get the node type from the data, default to 'Node'
    node_properties = data.get('properties', {})  # Get the node properties from the data

    # Create the node
    query = f"MERGE (n:{node_type} {{ title: '{node_properties.get('title')}', tagline: '{node_properties.get('tagline')}', released: {int(node_properties.get('released'))}}}) RETURN n"

    result = conn.query(query)

    return "Movie added!"

@api.route('/create_relation_SECUELADE', methods=['POST'])
def create_relation_SECUELADE():
    data = request.get_json()

    # Your API logic here
    start_node = data.get('start_node', {})
    end_node = data.get('end_node', {})
    relation_type = data.get('relation_type', 'SECUELA_DE')

    # Create the relation
    query = f"MERGE (m1:Movie {{title: '{start_node}'}}) MERGE (m2:Movie {{title: '{end_node}'}}) MERGE (m1)-[r:{relation_type}]->(m2) RETURN r"

    result = conn.query(query)

    return "Relation added!"
