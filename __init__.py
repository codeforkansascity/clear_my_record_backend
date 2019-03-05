from flask import Flask

cmr = Flask(__name__)

from cmr_backend import routes
