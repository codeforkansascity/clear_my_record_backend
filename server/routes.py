from flask import request, Response, abort, jsonify
from clear_my_record_backend.server import cmr, models, dbs
from clear_my_record_backend.server.schemas import user_schema, client_schema, clients_schema, conviction_schema, convictions_schema, charge_schema, charges_schema
from flask_jwt_extended import (jwt_required, create_access_token,
                                get_jwt_identity)
from flask_restful import Resource
from sqlalchemy import exc
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
        return Response("User with ID {} not found".format(user_id), status=404, mimetype='text/plain')
    result = user_schema.dump(usr)

    return jsonify(result.data)


@cmr.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # is there a way to filter params like you can in rails?
    if not request.json:
        return Response('No JSON data', status=400, mimetype='test/plain')

    usr = models.User.query.get(user_id)

    if usr is None:
        return Response("User with ID {} not found".format(user_id), status=404, mimetype='text/plain')

    updated_user = None

    try:
        updated_user = usr.update(request.json)
        dbs.session.commit()
    except AttributeError as err:
        # not ideal, but works for now
        dbs.session.rollback()
        return Response("{}".format(err), status=422, mimetype='text/plain')
    except exc.IntegrityError as err:
        # Do better with this
        dbs.session.rollback()
        return Response("{}".format(err), status=400, mimetype='text/plain')
    except Exception as err:
        # this will have to work for now
        dbs.session.rollback()
        return Response("Issue updating user with ID {}".format(user_id), status=500, mimetype='text/plain')

    if updated_user is None:
        return Response("Issue updating user with ID {}".format(user_id), status=500, mimetype='text/plain')


    dbs.session.flush()
    return jsonify(updated_user.id)


@cmr.route('/clients', methods=['POST'])
def add_client():
    client = models.Client()

    if request.json:
        try:
            client.update(request.json)
            dbs.session.add(client)
            dbs.session.commit()
            dbs.session.flush()
            return jsonify(client.id)
        except AttributeError as err:
            dbs.session.rollback()
            return Response("{}".format(err), status=422, mimetype='text/plain')
        except Exception as err:
            # this will have to work for now
            dbs.session.rollback()
            return Response("Issue adding new client", status=500, mimetype='text/plain')
    else:
        dbs.session.add(client)
        dbs.session.commit()
        dbs.session.flush()
        return jsonify(client.id)


@cmr.route('/clients', methods=['GET'])
def get_clients():
    cli = models.Client.query.all()
    if cli is None:
        return Response("Issue retreiving all clients".format(cli), status=404, mimetype='text/plain')
    result = clients_schema.dump(cli)

    return jsonify(result.data)


@cmr.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    cli = models.Client.query.get(client_id)
    if cli is None:
        return Response("Client with ID {} not found".format(client_id), status=404, mimetype='text/plain')
    result = client_schema.dump(cli)

    return jsonify(result.data)


@cmr.route('/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    if not request.json:
        return Response('No JSON data', status=400, mimetype='test/plain')

    client = models.Client.query.get(client_id)

    if client is None:
        return Response("Client with ID {} not found".format(client_id), status=404, mimetype='text/plain')

    updated_client = None

    try:
        updated_client = client.update(request.json)
        dbs.session.commit()
    except AttributeError as err:
        # not ideal, but works for now
        dbs.session.rollback()
        return Response("{}".format(err), status=422, mimetype='text/plain')
    except exc.IntegrityError as err:
        # Do better with this
        dbs.session.rollback()
        return Response("{}".format(err), status=400, mimetype='text/plain')
    except Exception as err:
        # this will have to work for now
        dbs.session.rollback()
        return Response("Issue updating client with ID {}".format(client_id), status=500, mimetype='text/plain')

    if updated_client is None:
        return Response("Issue updating client with ID {}".format(client_id), status=500, mimetype='text/plain')

    dbs.session.flush()
    return jsonify(updated_client.id)


@cmr.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    pass


@cmr.route('/clients/<int:client_id>/convictions', methods=['GET'])
def get_client_convictions(client_id):
    client_convictions = models.Conviction.query.filter(models.Client.id==client_id).all()
    if client_convictions is None:
        return Response("Could not find any convictions for Client {}".format(client_id, status=404, mimetype='text/plain'))
    result = convictions_schema.dump(client_convictions)

    return jsonify(result.data)


@cmr.route('/clients/<int:client_id>/convictions', methods=['POST'])
def add_client_conviction(client_id):
    client = models.Client.query.get(client_id)
    if client is None:
        return Response("Client with ID {} not found".format(client_id), status=404, mimetype='text/plain')

    conviction = models.Conviction()
    client.convictions.append(conviction)

    if request.json:
        try:
            conviction.update(request.json)
            dbs.session.add(conviction)
            dbs.session.commit()
            dbs.session.flush()
            return jsonify(conviction.id)
        except AttributeError as err:
            dbs.session.rollback()
            return Response("{}".format(err), status=422, mimetype='text/plain')
        except Exception as err:
            # this will have to work for now
            dbs.session.rollback()
            return Response("Issue adding new conviction for client {}".format(client_id), status=500, mimetype='text/plain')
    else:
        dbs.session.add(conviction)
        dbs.session.commit()
        dbs.session.flush()
        return jsonify(conviction.id)


@cmr.route('/convictions/<int:conviction_id>', methods=['GET'])
def get_conviction(conviction_id):
    conviction = models.Conviction.query.get(conviction_id)
    if conviction is None:
        return Response("Conviction with ID {} not found".format(conviction_id), status=404, mimetype='text/plain')
    result = conviction_schema.dump(conviction)

    return jsonify(result.data)


@cmr.route('/convictions/<int:conviction_id>', methods=['PUT'])
def update_conviction(conviction_id):
    if not request.json:
        return Response('No JSON data', status=400, mimetype='test/plain')

    conviction = models.Conviction.query.get(conviction_id)
    if conviction is None:
        return Response("Conviction with ID {} not found".format(conviction_id), status=404, mimetype='text/plain')

    updated_conviction = None

    try:
        updated_conviction = conviction.update(request.json)
        dbs.session.commit()
    except AttributeError as err:
        # not ideal, but works for now
        dbs.session.rollback()
        return Response("{}".format(err), status=422, mimetype='text/plain')
    except exc.IntegrityError as err:
        # Do better with this
        dbs.session.rollback()
        return Response("{}".format(err), status=400, mimetype='text/plain')
    except Exception as err:
        # this will have to work for now
        dbs.session.rollback()
        return Response("Issue updating conviction with ID {}".format(conviction_id), status=500, mimetype='text/plain')

    if updated_conviction is None:
        return Response("Issue updating client with ID {}".format(conviction_id), status=500, mimetype='text/plain')

    dbs.session.flush()
    return jsonify(updated_conviction.id)


@cmr.route('/convictions/<int:conviction_id>', methods=['DELETE'])
def delete_conviction(conviction_id):
    conviction = models.Conviction.query.get(conviction_id)
    pass


@cmr.route('/clients/<int:client_id>/convictions/<int:conviction_id>/charges', methods=['GET'])
def get_client_charges(client_id, conviction_id):
    charges = models.Charge.query.filter(models.Client.id==client_id and models.Conviction.id==conviction_id).all()
    if charges is None:
        return Response("Could not find charges for client {} and conviction {}".format(client_id, conviction_id), status=404, mimetype='text/plain')
    result = charges_schema.dump(charges)

    return jsonify(result.data)


@cmr.route('/clients/<int:client_id>/convictions/<int:conviction_id>/charges', methods=['POST'])
def add_client_charges(client_id, conviction_id):
    client_convictions = models.Conviction.query.filter(models.Client.id==client_id and models.Conviction.id==conviction_id)
    if client_convictions is None:
        pass

@cmr.route('/charges/<int:charge_id>', methods=['GET'])
def get_charge(charge_id):
    charge = models.Charge.query.get(charge_id)
    if charge is None:
        return Response("Could not find charge with ID {}".format(charge_id), status=404, mimetype='text/plain')

    result = charge_schema.dump(charge)

    return jsonify(result.data)


@cmr.route('/charges/<int:charge_id>', methods=['PUT'])
def update_charge(charge_id):
    pass


@cmr.route('/charges/<int:charge_id>', methods=['DELETE'])
def delete_charge(charge_id):
    pass
# don't forget to return id when doing post
