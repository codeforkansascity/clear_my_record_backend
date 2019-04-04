from flask import Flask
from clear_my_record_backend.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager

cmr = Flask(__name__)
cmr.config.from_object(Config)
dbs = SQLAlchemy(cmr)
migratate = Migrate(cmr, dbs)
CORS(cmr)
jwt = JWTManager(cmr)
api = Api(cmr)

# having this import here is key to avoid circular imports as well as
# being able to define  our API routes
from clear_my_record_backend.server import routes, models, resources

api.add_resource(resources.Register, '/register')
api.add_resource(resources.Login, '/login')
api.add_resource(resources.Me, '/me')
