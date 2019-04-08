from flask import request, Response, abort
from clear_my_record_backend.server import cmr, models, dbs
from flask_jwt_extended import (jwt_required, create_access_token,
                                get_jwt_identity)
from flask_restful import Resource
from datetime import datetime


@cmr.route('/')
@cmr.route('/index')
def index():
    return "Hello, World!"


@cmr.route('/qualifying_question', methods=['GET'])
def qualifying_question():
    pass


@cmr.route('/qualifying_questions', methods=['GET'])
def qualifying_questions():
    pass


@cmr.route('/qualifying_answer', methods=['POST'])
def qualifying_answer():
    if not request.json:
        return Response('No JSON data', status=400, mimetype='test/plain')

    qualifying_answer = {
        "user_session": request.json['user_session'],
        "question_id": request.json['question_id'],
        "answer": request.json['answer'],
        "qualifying_answer": request.json['qualifying_answer'],
        "question_version_number": request.json['question_version_number'],
        "timestamp": datetime.fromtimestamp(request.json['timestamp'] / 1000.0)
    }

    answer = models.Qualifying_Answer(qualifying_answer)
    dbs.session.add(answer)
    dbs.session.commit()

    return Response('Success', status=200, mimetype='text/plain')


@cmr.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    usr = models.User.query.get(user_id)
    if usr is None:
        return Response("User with ID {} not found".format(user_id))


@cmr.route('/users/<int:user_id>', methods=['POST'])
def update_user(user_id):
    # return id
    usr = models.User.query.get(user_id)
    pass


@cmr.route('/clients', methods=['POST'])
def add_client():
    # return id
    pass


@cmr.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    pass


@cmr.route('/clients/<int:client_id>', methods=['POST'])
def update_client(client_id):
    #return id
    pass


@cmr.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    pass


@cmr.route('/clents/<int:client_id>/convictions', methods=['GET'])
def get_client_convictions(client_id):
    client_convictions = Client.query.get(client_id).convictions
    pass


@cmr.route('/clients/<int:client_id>/convictions', methods=['POST'])
def add_client_conviction(client_id):
    # return id
    pass


@cmr.route('/convictions/<int:conviction_id>', methods=['GET'])
def get_conviction(conviction_id):
    conviction = Conviction.query.get(conviction_id)
    pass


@cmr.route('/convictions/<int:conviction_id>', methods=['POST'])
def update_conviction(conviction_id):
    # return id
    pass


@cmr.route('/convictions/<int:conviction_id>', methods=['DELETE'])
def delete_conviction(conviction_id):
    conviction = Conviction.query.get(conviction_id)
    pass


@cmr.route('/clients/<int:client_id>/convictions/<int:conviction_id>/charges', methods=['GET'])
def get_client_charges(client_id, conviction_id):
    pass


@cmr.route('/clients/<int:client_id>/convictions/<int:conviction_id>/charges', methods=['POST'])
def add_client_charges(client_id, conviction_id):
    pass


@cmr.route('/charges/<int:charge_id>', methods=['GET'])
def get_charge(charge_id):
    pass


@cmr.route('/charges/<int:charge_id>', methods=['PUT'])
def update_charge(charge_id):
    pass


@cmr.route('/charges/<int:charge_id>', methods=['DELETE'])
def delete_charge(charge_id):
    pass
# don't forget to return id when doing post
