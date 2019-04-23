from server import dbs
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum
from datetime import datetime

charge_types = Enum('CHARGE', 'FELONY MISDEMEANOR')
class_types = Enum('CLASS', 'A B C D E UNDEFINED')
user_types = Enum('USER', 'CLINIC_STAFF LAWYER CLIENT ADMIN SUPER_ADMIN')

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
    user_type = dbs.Column(dbs.String(64))
    clients = dbs.relationship('Client', backref='user', lazy='dynamic')
    created_at = dbs.Column(dbs.DateTime, default=datetime.utcnow)
    updated_at = dbs.Column(dbs.DateTime, default=datetime.utcnow)

    def __init__(self, *data, **kwargs):
        super(User, self).__init__(**kwargs)
        for dictionary in data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def update(self, *data, **kwargs):
        for dictionary in data:
            for key in dictionary:
                if not hasattr(self, key):
                    raise AttributeError("{} is not a valid field".format(key))
                try:
                    setattr(self, key, dictionary[key])
                except AssertionError:
                    raise AssertionError("{} is not a valid {}".format(dictionary[key], key))
        for key in kwargs:
            if not hasattr(self, key):
                raise AttributeError("{} is not a valid field".format(key))
            setattr(self, key, kwargs[key])
        return self

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

    @dbs.validates('user_type')
    def validate_user_type(self, key, user_type):
        assert str(user_type).replace(' ', '_').upper() in user_types.__members__
        return user_type

    @classmethod
    def find_by_email(cls, _email):
        return cls.query.filter_by(email=_email).first()

    @classmethod
    def find_by_username(cls, _username):
        return cls.query.filter_by(username=_username).first()

class Client(dbs.Model):
    id = dbs.Column(dbs.Integer, primary_key=True)
    user_id = dbs.Column(dbs.Integer, dbs.ForeignKey('user.id'))
    full_name = dbs.Column(dbs.String(128))
    # 123-456-7890
    phone = dbs.Column(dbs.VARCHAR(12))
    email = dbs.Column(dbs.String(128))
    sex = dbs.Column(dbs.String(16))
    race = dbs.Column(dbs.String(64))
    dob = dbs.Column(dbs.Date)
    address_line_1 = dbs.Column(dbs.String(64))
    address_line_2 = dbs.Column(dbs.String(64))
    city = dbs.Column(dbs.String(64))
    state = dbs.Column(dbs.String(64))
    # 64111 or 64111-0000
    zip_code = dbs.Column(dbs.VARCHAR(10))
    license_number = dbs.Column(dbs.String(64))
    license_issuing_state = dbs.Column(dbs.VARCHAR(2))
    license_expiration_date = dbs.Column(dbs.Date)
    status = dbs.Column(dbs.String(64))
    active = dbs.Column(dbs.Boolean)
    convictions = dbs.relationship('Conviction', backref='client', lazy='dynamic')
    created_at = dbs.Column(dbs.DateTime, default=datetime.utcnow)
    updated_at = dbs.Column(dbs.DateTime, default=datetime.utcnow)
    notes = dbs.Column(dbs.Text)
    filing_court = dbs.Column(dbs.String(64))
    judicial_circuit_number = dbs.Column(dbs.Text)
    county_of_prosecutor = dbs.Column(dbs.String(64))
    judge_name = dbs.Column(dbs.Text)
    division_name = dbs.Column(dbs.Text)
    petitioner_name = dbs.Column(dbs.Text)
    division_number = dbs.Column(dbs.Text)
    city_name_here = dbs.Column(dbs.Text)
    county_name = dbs.Column(dbs.Text)
    arresting_county = dbs.Column(dbs.Text)
    prosecuting_county = dbs.Column(dbs.Text)
    arresting_municipality = dbs.Column(dbs.Text)
    other_agencies_name = dbs.Column(dbs.Text)
    created_by = dbs.Column(dbs.Integer)
    modified_by = dbs.Column(dbs.Integer)
    purged_by = dbs.Column(dbs.Integer)
    # this is the number coming from the case management system
    # that's used as a prefilter/prescreen/starting point for all of these expungements
    cms_case_number = dbs.Column(dbs.VARCHAR(64))
    previous_expungements = dbs.Column(dbs.Text)

    def __init__(self, *data, **kwargs):
        super(Client, self).__init__(**kwargs)
        for dictionary in data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def update(self, *data, **kwargs):
        for dictionary in data:
            for key in dictionary:
                if not hasattr(self, key):
                    raise AttributeError("{} is not a valid field".format(key))
                try:
                    setattr(self, key, dictionary[key])
                except AssertionError:
                    raise AssertionError("{} is not a valid {}".format(dictionary[key], key))
        for key in kwargs:
            if not hasattr(self, key):
                raise AttributeError("{} is not a valid field".format(key))
            setattr(self, key, kwargs[key])
        return self


class Conviction(dbs.Model):
    id = dbs.Column(dbs.Integer, primary_key=True)
    client_id = dbs.Column(dbs.Integer, dbs.ForeignKey('client.id'))
    case_number = dbs.Column(dbs.String(64))
    agency = dbs.Column(dbs.String(64))
    court_name = dbs.Column(dbs.String(64))
    court_city_county = dbs.Column(dbs.String(64))
    judge = dbs.Column(dbs.String(128))
    record_name = dbs.Column(dbs.String(128))
    release_status = dbs.Column(dbs.String(64))
    release_date = dbs.Column(dbs.Date)
    charges = dbs.relationship('Charge', backref='conviction', lazy='dynamic')
    created_at = dbs.Column(dbs.DateTime, default=datetime.utcnow)
    updated_at = dbs.Column(dbs.DateTime, default=datetime.utcnow)
    notes = dbs.Column(dbs.Text)
    name = dbs.Column(dbs.String(128))
    arrest_date = dbs.Column(dbs.String(64))
    created_by = dbs.Column(dbs.String(128))

    def __init__(self, *data, **kwargs):
        super(Conviction, self).__init__(**kwargs)
        for dictionary in data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def update(self, *data, **kwargs):
        for dictionary in data:
            for key in dictionary:
                if not hasattr(self, key):
                    raise AttributeError("{} is not a valid field".format(key))
                try:
                    setattr(self, key, dictionary[key])
                except AssertionError:
                    raise AssertionError("{} is not a valid {}".format(dictionary[key], key))
        for key in kwargs:
            if not hasattr(self, key):
                raise AttributeError("{} is not a valid field".format(key))
            setattr(self, key, kwargs[key])
        return self

class Charge(dbs.Model):
    id = dbs.Column(dbs.Integer, primary_key=True)
    conviction_id = dbs.Column(dbs.Integer, dbs.ForeignKey('conviction.id'))
    charge = dbs.Column(dbs.String(128))
    citation = dbs.Column(dbs.String(128))
    sentence = dbs.Column(dbs.String(128))
    conviction_class_type = dbs.Column(dbs.String(64))
    conviction_charge_type = dbs.Column(dbs.String(64))
    eligible = dbs.Column(dbs.String(64))
    please_expunge = dbs.Column(dbs.String(64))
    created_at = dbs.Column(dbs.DateTime, default=datetime.utcnow)
    updated_at = dbs.Column(dbs.DateTime, default=datetime.utcnow)
    notes = dbs.Column(dbs.Text)
    conviction_description = dbs.Column(dbs.String(256))
    to_print = dbs.Column(dbs.Text)
    convicted = dbs.Column(dbs.String(64))

    def __init__(self, *data, **kwargs):
        super(Charge, self).__init__(**kwargs)
        for dictionary in data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    # @dbs.validates('conviction_class_type')
    # def validate_class_type(self, key, class_type):
    #     assert str(class_type).replace(' ', '_').upper() in class_types.__members__
    #     return class_type

    # @dbs.validates('conviction_charge_type')
    # def validate_charge_type(self, key, charge_type):
    #     assert str(charge_type).upper() in charge_types.__members__
    #     return charge_type

    def update(self, *data, **kwargs):
        for dictionary in data:
            for key in dictionary:
                if not hasattr(self, key):
                    raise AttributeError("{} is not a valid field".format(key))
                try:
                    setattr(self, key, dictionary[key])
                except AssertionError:
                    raise AssertionError("{} is not a valid {}".format(dictionary[key], key))
        for key in kwargs:
            if not hasattr(self, key):
                raise AttributeError("{} is not a valid field".format(key))
            setattr(self, key, kwargs[key])
        return self
