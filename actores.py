from flask import Blueprint, request, jsonify
from flask_restful import Resource, reqparse
from neo4j import GraphDatabase, RoutingControl
from flask import request, jsonify
from Neo4jConnection import Neo4jConnection

import json
from datetime import date

api = Blueprint('actores', __name__)

conn = Neo4jConnection()

@api.route('/', methods=['GET'])
def home():
    return "Aqui se encuentran los actores"

@api.route('/info', methods=['GET'])
def info():
    results = conn.query("MATCH (a:Actor) RETURN a LIMIT 5")
    actores = []
    for result in results:
        new_result = result['a']

        # Extract properties
        properties = dict(new_result)
        date = properties['yearBorn']
        python_date = date.to_native()
        js_date_string = python_date.strftime('%Y-%m-%d')
        properties['yearBorn'] = js_date_string
        actores.append(properties)

    return actores

@api.route('/send', methods=['POST'])
def send_data():
    data = request.get_json()

    print(data)
    # Your API logic here
    return "Actors data received!"
