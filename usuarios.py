from flask import Blueprint, request, jsonify
from flask_restful import Resource, reqparse
from neo4j import GraphDatabase, RoutingControl, time
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from datetime import date

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

@api.route('/info/<int:page>', methods=['GET'])
def info(page):
    results = queries.find_node_range(["Usuario"], [], page * 15, 15)
    usuarios = []
    for result in results:
        new_result = result['n']

        # Extract properties
        properties = dict(new_result)
        # Verificar si 'yearBorn' está presente en properties antes de acceder a él
        if 'yearBorn' in properties:
            date = properties['yearBorn']
            python_date = date.to_native()
            js_date_string = python_date.strftime('%Y-%m-%d')
            properties['yearBorn'] = js_date_string
        else:
            # Si 'yearBorn' no está presente, puedes establecer un valor predeterminado o manejarlo según tu lógica
            properties['yearBorn'] = 'N/A'  # Por ejemplo, establecer 'N/A' si no hay año de nacimiento
        usuarios.append(properties)

    return jsonify(usuarios)
    
@api.route('/relations/<string:label>', methods=['GET'])
def getRelsProps(label):
    data = request.args.to_dict()
    print(request.args)
    
    nombre = data.get("nombre")
    apellido = data.get("apellido")

    relaciones = [] 
    results = queries.list_relations(["Usuario"],[('nombre',nombre), ('apellido',apellido)],[],[],label)

    for result in results:
        rel_result = result['r']
        properties = dict(rel_result)
        for key, value in properties.items():
            if isinstance(value, time.Date):
                properties[key] = value.to_native().strftime('%Y-%m-%d')
        
        dest_node_result = result['n2']
        node_properties = dict(dest_node_result)
        for key, value in node_properties.items():
            if isinstance(value, time.Date):
                node_properties[key] = value.to_native().strftime('%Y-%m-%d')
        properties.update(node_properties)
        
        relaciones.append(properties)
        final = [i for n, i in enumerate(relaciones) if i not in relaciones[:n] ]
    
    return jsonify(final)
    

@api.route('/setNodeProps', methods=['PATCH'])
def setNodeProps():
    data = request.get_json()
    usuarios = data['data']
    
    for user in usuarios:
        match = [
            ('correo', user['correo'])
        ]
        props = [
            ('nombre', user['nombre']),
            ('apellido', user['apellido']),
            ('edad', user['edad']),
            ('genero', user['genero']),
            ('pais', user['pais']),
            ('preferencias', user['preferencias'])
        ]
        result = queries.set_node_props("Usuario", props, match)
        print(result)
    
    return "Successful update"

@api.route('/setRelsProps/<string:label>', methods=['PATCH'])
def setRelsProps(label):
    data = request.get_json()
    
    rels = data['data']
    
    match = [('nombre', data['nombre']), ('apellido', data['apellido'])]
    for r in rels:
        props = []
        match2 = []
        
        type = ""
        if label == "AMIGO":
            type = "Usuario"
            for k, v in r.items():
                if k not in ["fecha", "seguido", "amigo"]:
                    match2.append((k, v))
                else:
                    props.append((k, v))
        elif label == "WATCHED":
            type = "Pelicula"
            for k, v in r.items():
                if k not in ["watchedDate", "rating", "favorite"]:
                    match2.append((k, v))
                else:
                    props.append((k, v))
        elif label == "LIKED_ACTOR":
            type = "Actor"
            for k, v in r.items():
                if k not in ["fecha", "calificacion", "isPublic"]:
                    match2.append((k, v))
                else:
                    props.append((k, v))
        elif label == "LIKED_DIRECTOR":
            type = "Director"
            for k, v in r.items():
                if k not in ["fecha", "calificacion", "isPublic"]:
                    match2.append((k, v))
                else:
                    props.append((k, v))
        elif label == "LIKED_GENRE":
            type = "Genero"
            for k, v in r.items():
                if k not in ["fecha", "preferencia", "amigo"]:
                    match2.append((k, v))
                else:
                    props.append((k, v))
    
        result = queries.set_relation_props(label, props, "Usuario", type, match, match2)
        print(result)
    
    return "Succesfull update"
        
    
    
    
    