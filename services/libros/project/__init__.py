# services/users/project/__init__.py


import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


# instanciado la db
db = SQLAlchemy()


# new
def create_app(script_info=None):

    # instanciando la app
    app = Flask(__name__)
    # enable CORS
    CORS(app)

    # estableciendo configuracion
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # configurando extensiones
    db.init_app(app)

    # registro blueprints
    from project.api.libros import libros_blueprint
    app.register_blueprint(libros_blueprint)

    # contexto de shell for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
