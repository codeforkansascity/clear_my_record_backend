from clear_my_record_backend.server import dbs
from werkzeug.security import generate_password_hash, check_password_hash


class Qualifying_Question(dbs.Model):
    id = dbs.Column(dbs.Integer, primary_key=True)
    question = dbs.Column(dbs.Text)
    help_text = dbs.Column(dbs.Text)
    disqualifying_answer = dbs.Column(dbs.String(250))


class Qualifying_Answer(dbs.Model):
    # First Integer ID is set as autoincrement in SQLAlchemy
    id = dbs.Column(dbs.Integer, primary_key=True)
    user_session = dbs.Column(dbs.String(250), index=True, unique=False)
    question_id = dbs.Column(dbs.String(250))
    answer = dbs.Column(dbs.Text)
    qualifying_answer = dbs.Column(dbs.String(250))
    question_version_number = dbs.Column(dbs.Float(asdecimal=True))
    timestamp = dbs.Column(dbs.DateTime, index=True)
    answerer_id = dbs.Column(dbs.Integer, dbs.ForeignKey("user.id"))

    def __init__(self, *data, **kwargs):
        super(Qualifying_Answer, self).__init__(**kwargs)
        for dictionary in data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])


class User(dbs.Model):
    id = dbs.Column(dbs.Integer, primary_key=True)
    username = dbs.Column(dbs.String(32), index=True, unique=True)
    email = dbs.Column(dbs.String(120), index=True, unique=True)
    pw_hash = dbs.Column(dbs.String(128))
    submissions = dbs.relationship(
        "Qualifying_Answer", backref="author", lazy="dynamic")

    def __init__(self, *data, **kwargs):
        super(User, self).__init__(**kwargs)
        for dictionary in data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __repr__(self):
        return "<USER: {}>".format(self.username)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def exists(self):
        name = User.query.filter_by(username=self.username).first()
        email = User.query.filter_by(email=self.email).first()
        return name is not None or email is not None

    @classmethod
    def find_by_email(cls, _email):
        return cls.query.filter_by(email=_email).first()

    @classmethod
    def find_by_username(cls, _username):
        return cls.query.filter_by(username=_username).first()
