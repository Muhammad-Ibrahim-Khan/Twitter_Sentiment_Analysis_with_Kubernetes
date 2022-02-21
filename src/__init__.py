from flask import Flask
from src.controller import process
from flask_cors import CORS

service = Flask(__name__)

cors = CORS(service, resources={r"/*": {"origins": "http://0.0.0.0:5000"}})

service.register_blueprint(process)
