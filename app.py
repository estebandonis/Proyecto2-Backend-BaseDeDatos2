# app.py
from flask import Flask
from flask_cors import CORS

from movies import api as movies_api
from actors import api as actors_api

app = Flask(__name__)
app.register_blueprint(movies_api, url_prefix='/api/movies')  # Register the blueprint
app.register_blueprint(actors_api, url_prefix='/api/actors')  # Register the blueprint
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
