from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app,   resources={r"/gpt": {
    "origins": ["http://localhost:3000","http://127.0.0.1:3000"]}})         