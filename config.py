import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DBS_URL') or \
        'sqlite:////' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # DEV ONLY
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'enter-the-shaolin'
