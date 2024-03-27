from neo4j import GraphDatabase, RoutingControl
from dotenv import load_dotenv

import os

load_dotenv(".env")

uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USER")
password = os.getenv("NEO4J_PASSWORD")

class Neo4jConnection:
    def __init__(self):
        self._uri = uri
        self._username = username
        self._password = password
        self._driver = None

        try:
            self._driver = GraphDatabase.driver(self._uri, auth=(self._username, self._password))
            print("Driver created.")
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self._driver is not None:
            self._driver.close()
            print("Driver closed.")

    def query(self, query, parameters=None, db="neo4j"):

        assert self._driver is not None, "Driver not initialized!"
        session = None
        response = None

        try:
            session = self._driver.session(database=db) if db else self._driver.session()
            response = list(session.run(query, parameters))
        except Exception as e:
            print(f"Query failed: {e}")
        finally:
            if session is not None:
                session.close()
        return response
