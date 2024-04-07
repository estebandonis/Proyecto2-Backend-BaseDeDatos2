from flask import Blueprint, request, jsonify
from flask_restful import Resource, reqparse
from neo4j import GraphDatabase, RoutingControl
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from Neo4jConnection import Neo4jConnection

import json

api = Blueprint('usuarios', __name__)
cors = CORS(api)

conn = Neo4jConnection()

@api.route('/', methods=['GET'])
def home():
    return "Aqui se encuentran los usuarios"

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    results = conn.query(f"MATCH (u:Usuario {{correo: '{data['correo']}', contraseña: '{data['contra']}'}}) RETURN u.correo")

    return "true" if results != [] else "false"
