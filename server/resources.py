from flask_restful import Resource


class Register(Resource):
    def post(self):
        return {'message': 'Register'}


class UserLogin(Resource):
    def post(self):
        return {'message': 'User Login'}
