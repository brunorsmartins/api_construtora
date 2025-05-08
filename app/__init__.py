from flask import Flask
from .db import mongo
from app.routes import register_routes
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    mongo.init_app(app)
    register_routes(app)
    return app
