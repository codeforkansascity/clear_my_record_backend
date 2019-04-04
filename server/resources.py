from flask import request, abort, Response
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, create_access_token,
                                get_jwt_identity)
from clear_my_record_backend.server.models import User, save_to_dbs

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
            abort(400)

        try:
            save_to_dbs(new_user)
            msg = "Success. User {} created".format(new_user.username)
            return Response(msg, status=200, mimetype='text/plain')
        except SQLAlchemyError as e:

            msg = "Error while updating database: {}".format(e)
            return Response(msg, status=500)
        except Exception as e:
            # TODO: Try to get something more specific here for debuggin, etc.
            msg = "Unanticipated Error: {}".format(e)
            return Response(msg, status=500)

class Login(Resource):
    def post(self):
        return {'message': 'User Login'}


class Me(Resource):
    def get(self):
        return {'message': 'what do you want'}

    def post(self):
        return {'message': 'yep it is you, the user'}
