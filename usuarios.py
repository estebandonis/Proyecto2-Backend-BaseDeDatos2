from flask import Blueprint, request, jsonify
from flask_restful import Resource, reqparse
from neo4j import GraphDatabase, RoutingControl
from flask import request, jsonify
from flask_cors import CORS, cross_origin

import queries
import json

api = Blueprint('usuarios', __name__)
cors = CORS(api)

@api.route('/', methods=['GET'])
def home():
    return "Aqui se encuentran los usuarios"

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    results = queries.find_node(["Usuario"], [("correo", data['correo']), ("contraseña", data['contra'])])
    user = {}
    if results != []:
        for result in results:
            new_result = result['n']

            # Extract properties
            properties = dict(new_result)
            user['correo'] = properties['correo']
            user['nombre'] = properties['nombre']
            user['apellido'] = properties['apellido']
            user['edad'] = properties['edad']
            user['pais'] = properties['pais']
            user['genero'] = properties['genero']
            user['preferencias'] = properties['preferencias']
            break

    return user if results != [] else "false"
