# app.py
from flask import Flask
from flask_cors import CORS

from peliculas import api as peliculas_api
from actores import api as actores_api
from usuarios import api as usuarios_api

app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'
app.register_blueprint(peliculas_api, url_prefix='/api/peliculas')
app.register_blueprint(actores_api, url_prefix='/api/actores')
app.register_blueprint(usuarios_api, url_prefix='/api/usuarios')
cors = CORS(app)

@app.route('/api', methods=['GET'])
def home():
    return "Hello, World!"


if __name__ == '__main__':
    app.run(debug=True)
