from flask import request, abort, Response, jsonify
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, create_access_token,
                                create_refresh_token, get_jwt_identity)
from clear_my_record_backend.server.models import User, save_to_dbs, dbs


class Register(Resource):
    def post(self):
        if not request.json:
            abort(400)

        new_user = User(
            username=request.json['username'],
            email=request.json['email'],
        )
        new_user.set_password(request.json['password'])

        if new_user.exists():
            # TODO: some better exception handlers
            # This clumps both existing emails and usernames, separate erros.
            msg = "Failure: User already exists."
            return Response(msg, status=400, mimetype='text/plain')
            # abort(400)

        try:
            save_to_dbs(new_user)
            msg = "Success. User {} created".format(new_user.username)
            # return Response(msg, status=200, mimetype='text/plain')
        except SQLAlchemyError as e:
            msg = "Error while updating database: {}".format(e)
            return Response(msg, status=500)
        except Exception as e:
            # TODO: Try to get something more specific here for debuggin, etc.
            msg = "Unanticipated Error: {}".format(e)
            return Response(msg, status=500)

        token = create_access_token(identity=new_user.username)
        refresh = create_refresh_token(identity=new_user.username)
        data = {'status': "success", 'data': {
            'type': "bearer",
            'token': token,
            'refreshToken': refresh}}
        # causes error lol
        return data


class Login(Resource):
    def post(self):
        u = User.find_by_email(request.json['email'])
        if u:
            if u.check_password(request.json['password']):
                token = create_access_token(identity=u.username)
                refresh = create_refresh_token(identity=u.username)
                data = {'status': "success", 'data': {
                    'type': "bearer",
                    'token': token,
                    'refreshToken': refresh}}
                return data
            # TODO better error!
            return "made it inside at least"
        # TODO better error!
        return "nope"


class Me(Resource):
    def get(self):
        return {'message': 'what do you want'}

    def post(self):
        return {'message': 'yep it is you, the user'}
