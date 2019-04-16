from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow

dbs = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
cors = CORS()
jwt = JWTManager()


def create_app(config_class=Config):
    cmr = Flask(__name__)
    cmr.config.from_object(config_class)

    dbs.init_app(cmr)
    migrate.init_app(cmr, dbs)
    ma.init_app(cmr)
    cors.init_app(cmr)
    jwt.init_app(cmr)

    from server.core import core_bp
    cmr.register_blueprint(core_bp)

    from server.auth import auth_bp

    api = Api(auth_bp)
    api.add_resource(resources.Register, '/register')
    api.add_resource(resources.Login, '/login')
    api.add_resource(resources.Me, '/me')

    cmr.register_blueprint(auth_bp)

    return cmr

# having this import here is key to avoid circular imports as well as
# being able to define  our API routes
from server import models
# from clear_my_record_backend.server.core import routes

from server.auth import resources
