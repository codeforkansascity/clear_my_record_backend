from flask import request
from flask_restful import Resource


class Register(Resource):
    def post(self):
        return {'message': {'username': request.json['username'],
                            'email': request.json['email'],
                            'password': request.json['password']}}


class Login(Resource):
    def post(self):
        return {'message': 'User Login'}


class Me(Resource):
    def get(self):
        return {'message': 'what do you want'}

    def post(self):
        return {'message': 'yep it is you, the user'}
