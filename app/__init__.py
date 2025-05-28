from flask import Flask
from flask_restx import Api
from .db import mongo
from dotenv import load_dotenv
import os
from flask_cors import CORS




# Namespaces importados
from app.routes.cliente_routes import ns as cliente_ns
from app.routes.obra_routes import ns as obra_ns
from app.routes.orcamento_routes import ns as orcamento_ns 
from app.routes.receita_routes import ns as receita_ns 
from app.routes.gasto_routes import ns as gasto_ns
from app.routes.extra_routes import ns as extra_ns


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    # Configuração do Mongo via .env
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    mongo.init_app(app)
    CORS(app, supports_credentials=True,
         resources={r"/*": {"origins": "http://localhost:3000"}})

    # Swagger via Flask-RESTX
    api = Api(
        app,
        version="1.0",
        title="API da Empreiteira",
        description="Documentação interativa da API usando Swagger (Flask-RESTX)",
        doc="/docs",
        strict_slashes=False
        
    )

    # Registro dos namespaces
    api.add_namespace(cliente_ns)
    api.add_namespace(obra_ns)
    api.add_namespace(orcamento_ns)
    api.add_namespace(receita_ns)
    api.add_namespace(gasto_ns)
    api.add_namespace(extra_ns)

    return app
