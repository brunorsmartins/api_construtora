from .cliente_routes import cliente_bp
from .obra_routes import obra_bp
from .orcamento_routes import orcamento_bp
from .receita_routes import receita_bp
from .gasto_routes import gasto_bp
from .extra_routes import extra_bp

def register_routes(app):
    app.register_blueprint(cliente_bp)
    app.register_blueprint(obra_bp)
    app.register_blueprint(orcamento_bp)
    app.register_blueprint(receita_bp)
    app.register_blueprint(gasto_bp)
    app.register_blueprint(extra_bp)

