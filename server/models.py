from datetime import datetime
from clear_my_record_backend.server import dbs


class Qualifying_Question(dbs.Model):
    id = dbs.Column(dbs.Integer, primary_key=True)
    question = dbs.Column(dbs.Text)
    help_text = dbs.Column(dbs.Text)
    disqualifying_answer = dbs.Column(dbs.String(250))


class Qualifying_Answer(dbs.Model):
    # First Integer ID is set as autoincrement in SQLAlchemy
    id = dbs.Column(dbs.Integer, primary_key=True)
    user_session = dbs.Column(dbs.String(250), index=True, unique=True)
    question_id = dbs.Column(dbs.String(250))
    answer = dbs.Column(dbs.Text)
    qualifying_answer = dbs.Column(dbs.String(250))
    question_version_number = dbs.Column(dbs.Float(asdecimal=True))
    timestamp = dbs.Column(dbs.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, *data, **kwargs):
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
        "Submission", backef="author", lazy="dynamic")

    def __repr__(self):
        return "<USER: {}".format(self.username)


class Submission(dbs.Model):
    id = dbs.Column(dbs.Integer, primary_key=True)
    submitter_id = dbs.Column(dbs.Integer, dbs.ForeignKey("users.id"))
    session_sub = dbs.Column(dbs.Integer, dbs.Foreign("qualifying_answers.id"))
