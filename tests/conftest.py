import pytest

from os import environ

from config import Config
from server import dbs, create_app
from server.models import User


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


class TestProdConfig(Config):
    Testing = True
    SQLALCHEMY_DATABASE_URI = environ.get('TEST_DBS_URL')


class ProdTestConfig(Config):
    pass


@pytest.fixture()
def new_user():
    u = User(
        username="John Doe",
        email="john.doe@example.com")
    u.set_password("Password1234567890!")

    return u


@pytest.fixture(scope="module")
def _cmr():
    cmr = create_app(TestConfig)

    with cmr.app_context():
        dbs.create_all()

        yield cmr

        dbs.session.remove()
        dbs.drop_all()


@pytest.fixture(scope="module")
def _dbs():
    cmr = create_app(TestConfig)

    with cmr.app_context():
        dbs.create_all()

        yield dbs

        dbs.session.remove()
        dbs.drop_all()
