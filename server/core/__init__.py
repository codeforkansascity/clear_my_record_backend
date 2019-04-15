from flask import Blueprint

core_bp = Blueprint("core", __name__)

from clear_my_record_backend.server.core import routes
