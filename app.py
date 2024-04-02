# app.py
from flask import Flask
from flask_cors import CORS

from peliculas import api as peliculas_api
from actores import api as actores_api

app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'
app.register_blueprint(peliculas_api, url_prefix='/api/peliculas')  # Register the blueprint
app.register_blueprint(actores_api, url_prefix='/api/actores')  # Register the blueprint
cors = CORS(app)

@app.route('/api/', methods=['GET'])
def home():
    return "Hello, World!"


if __name__ == '__main__':
    app.run(debug=True)
