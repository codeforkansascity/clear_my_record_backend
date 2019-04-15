import pytest

from clear_my_record_backend.config import Config
from clear_my_record_backend.server.models import User
from clear_my_record_backend.server import dbs, create_app


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


@pytest.fixture()
def new_user():
    u = User(
        username="John Doe",
        email="john.doe@example.com")
    u.set_password("Password1234567890!")

    return u


@pytest.fixture(scope="module")
def app():
    cmr = create_app(TestConfig)
    with cmr.app_context():
        dbs.create_all()
        yield cmr
        dbs.session.remove()
        dbs.drop_all()
