from datetime import datetime

from neo4j import Query
from Neo4jConnection import Neo4jConnection

conn = Neo4jConnection()

def is_date(string, date_format="%Y-%m-%d"):
    try:
        datetime.strptime(string, date_format)
        return True
    except ValueError:
        return False

def getFields(fields):
    fields_string = ""
    for num, field in enumerate(fields):
        if type(field[1]) == str:
            if is_date(field[1]):
                fields_string += f"{field[0]}: date('{field[1]}')"
            else:
                fields_string += f"{field[0]}: '{field[1]}'"
        elif type(field[1]) == int or type(field[1]) == float or type(field[1]) == bool or type(field[1]) == list or type(field[1]) == dict:
            fields_string += f"{field[0]}: {field[1]}"

        if num != len(fields) - 1:
            fields_string += ", "

    return fields_string

def getTypes(types):
    types_string = ""
    for num, type in enumerate(types):
        types_string += f"{type}"
        if num != len(types) - 1:
            types_string += ":"

    return types_string

def create_node(type, fields):
    string_fields = getFields(fields)
    string_types = getTypes(type)
    conn.query(f"MERGE (n:{string_types} {{{string_fields}}})")

#crear nodo con 1 label
def create_node_with_single_label(label):
    query = f"CREATE (n:{label})"
    conn.query(query)
    print(f"Nuevo nodo con la label '{label}' creado")

#Creación de nodos con 2+ labels
def create_node_with_multiple_labels(labels):
    labels_string = ":".join(labels)
    query = f"CREATE (n:{labels_string})"
    conn.query(query)
    print(f"Nuevo nodo con las labels '{labels_string}' creadas")

#creacion de nodos con propiedades
def create_node_with_properties(label, properties):
    properties_string = getFields(properties)
    query = f"CREATE (n:{label} {{{properties_string}}})"
    conn.query(query)
    print(f"Nuevo nodo con la label '{label}' y propiedades creadas")

#eliminar nodo con nombre
def delete_node_by_name(label, name):
    query = f"MATCH (n:{label} {{nombre: '{name}'}}) DELETE n"
    conn.query(query)
    print(f"Nodo con nombre '{name}' y label '{label}' eliminado")

#eliminar varios nodos con nombre
def delete_nodes_by_name(label, names):
    names_string = "','".join(names)
    query = f"MATCH (n:{label}) WHERE n.nombre IN ['{names_string}'] DELETE n"
    conn.query(query)
    print(f"Nodos con nombres '{names}' y label '{label}' eliminados")

#eliminar relación con ID
def delete_relationship(relationship_id):
    query = f"MATCH ()-[r]->() WHERE id(r) = {relationship_id} DELETE r"
    conn.query(query)
    print(f"Relación con ID {relationship_id} eliminada")

#eliminar varias relaciones con ID
def delete_relationships_multiple(relationship_ids):
    ids_string = ",".join(str(id) for id in relationship_ids)
    query = f"MATCH ()-[r]->() WHERE id(r) IN [{ids_string}] DELETE r"
    conn.query(query)
    print(f"Relaciones con IDs {relationship_ids} eliminadas")


def create_relation(node1, value1, node2, value2, relation, fields):
    if fields != []:
        string_fields = getFields(fields)
        query = f"MATCH (n1:{node1} {{{value1[0]}:{value1[1]}}}), (n2:{node2} {{{value2[0]}:{value2[1]}}}) MERGE (n1)-[r:{relation} {{{string_fields}}}]->(n2)"
        conn.query(query)
        print(query)
    else:
        query = f"MATCH (n1:{node1} {{{value1[0]}:{value1[1]}}}), (n2:{node2} {{{value2[0]}:{value2[1]}}}) MERGE (n1)-[r:{relation}]->(n2)"
        conn.query(query)
        print(query)

def find_relation(node1, fields1, node2, fields2, relation):
    string_types1 = getTypes(node1)
    string_fields1 = getFields(fields1)
    string_types2 = getTypes(node2)
    string_fields2 = getFields(fields2)
    query = ""

    if fields1 != [] and fields2 != []:
        query = f"MATCH (n1:{string_types1} {{{string_fields1}}}), (n2:{string_types2} {{{string_fields2}}}) MATCH (n1)-[r:{relation}]->(n2) RETURN n1, n2"
    elif fields1 == []:
        query = f"MATCH (n1:{string_types1})-[r:{relation}]-(n2:{string_types2} {{{string_fields2}}}) RETURN n1, n2"
    elif fields2 == []:
        query = f"MATCH (n1:{string_types1} {{{string_fields1}}})-[r:{relation}]-(n2:{string_types2}) RETURN n1, n2"
    else:
        query = f"MATCH (n1:{string_types1} {{{string_fields1}}}), (n2:{string_types2} {{{string_fields2}}}) MATCH (n1)-[r:{relation}]->(n2) RETURN n1, n2"

    print(query)
    return conn.query(query)

def find_node(type, fields):
    string_types = getTypes(type)
    string_fields = getFields(fields)
    query = f"MATCH (n:{string_types} {{{string_fields}}}) RETURN n"
    print(query)
    return conn.query(query)

def set_node_props(type, props, match=[]):
    query = f"MATCH (n:{type}"
    if match != []:
        query += f" {{{getFields(match)}}}"
    query += f") SET n += {{{getFields(props)}}} RETURN n"
    print(query)
    return conn.query(query)

def set_relation_props(relation, props, type1, type2, match1=[], match2=[]):
    query = f"MATCH (n:{type1}"
    if match1 != []:
        query += f" {{{getFields(match1)}}}"
    query += f"), (m:{type2} "
    if match2 != []:
        query += f" {{{getFields(match2)}}}"
    query += f") MATCH (n1)-[r:{relation}]-(n2)"
    query += f" SET r += {{{getFields(props)}}} RETURN n, r, m"
    print(query)
    return conn.query(query)

        

def find_movies_by_genre(genre):
    query = f"""MATCH (n)-[r:WATCHED]->(p:Pelicula)-[r1:PERTENECE_A]->(g:Genero {{nombre: '{genre}'}})
    WITH p AS Peliculas, collect(r.rating) AS RATING
    RETURN Peliculas, reduce(total = 0, n IN RATING | total + n) / size(RATING) AS AVERAGE_RATING
    ORDER BY AVERAGE_RATING DESC"""
    return conn.query(query)
