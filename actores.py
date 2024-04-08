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

@api.route('/info', methods=['GET'])
def info():
    results = queries.find_node(["Actor"], [("nombre","Dora"), ("apellido", "Bankhead")])
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

    return actores

@api.route('/send', methods=['POST'])
def send_data():
    data = request.get_json()

    print(data)
    # Your API logic here
    return "Actors data received!"
