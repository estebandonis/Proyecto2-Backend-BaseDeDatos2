from flask import Blueprint, request, jsonify
from flask_restful import Resource, reqparse
from neo4j import GraphDatabase, RoutingControl
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from datetime import date
import json

import queries

api = Blueprint('actores', __name__)
cors = CORS(api)

@api.route('/', methods=['GET'])
def home():
    return "Aqui se encuentran los actores"

@api.route('/create_single_label_node', methods=['POST'])
def create_single_label_node():
    data = request.get_json()
    label = data['label']
    queries.create_node_with_single_label(label)
    return "Nuevo nodo creado con una label"

@api.route('/create_multi_label_node', methods=['POST'])
def create_multi_label_node():
    data = request.get_json()
    labels = data['labels']
    queries.create_node_with_multiple_labels(labels)
    return "Nuevo nodo creado con múltiples labels"

@api.route('/create_node_with_properties', methods=['POST'])
def create_node_with_props():
    data = request.get_json()
    label = data['label']
    properties = data['properties']
    queries.create_node_with_properties(label, properties)
    return "Nuevo nodo creado con propiedades"

@api.route('/delete_node_by_name', methods=['DELETE'])
def delete_node_by_name_route():
    data = request.get_json()
    label = data['label']
    name = data['name']
    queries.delete_node_by_name(label, name)
    return f"Nodo con nombre '{name}' y label '{label}' eliminado"

@api.route('/delete_nodes_by_names', methods=['DELETE'])
def delete_nodes_by_names_route():
    data = request.get_json()
    label = data['label']
    names = data['names']
    queries.delete_nodes_by_name(label, names)
    return f"Nodos con nombres '{names}' y label '{label}' eliminados"

@api.route('/delete_relationship/<int:relationship_id>', methods=['DELETE'])
def delete_relationship_by_id(relationship_id):
    queries.delete_relationship(relationship_id)
    return f"Relación con ID {relationship_id} eliminada"

@api.route('/delete_relationships', methods=['DELETE'])
def delete_multiple_relationships():
    data = request.get_json()
    relationship_ids = data['relationship_ids']
    queries.delete_relationships_multiple(relationship_ids)
    return f"Relaciones con IDs {relationship_ids} eliminadas"

@api.route('/info', methods=['GET'])
def info():
    results = queries.find_node(["Actor"], [])
    actores = []
    for result in results:
        new_result = result['n']

        # Extract properties
        properties = dict(new_result)
        date = properties['yearBorn']
        python_date = date.to_native()
        js_date_string = python_date.strftime('%Y-%m-%d')
        properties['yearBorn'] = js_date_string
        actores.append(properties)

    return jsonify(actores)

@api.route('/send', methods=['POST'])
def send_data():
    data = request.get_json()

    print(data)
    # Your API logic here
    return "Actors data received!"
