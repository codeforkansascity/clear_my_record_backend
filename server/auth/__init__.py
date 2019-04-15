from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from clear_my_record_backend.server.auth import resources
