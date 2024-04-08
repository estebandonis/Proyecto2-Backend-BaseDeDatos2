from datetime import datetime
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
