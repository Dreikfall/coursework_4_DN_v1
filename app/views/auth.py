from flask_restx import Namespace, Resource
from flask import request
from app.implemented import auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/register')
class AuthView(Resource):
    def post(self):
        data = request.json

        email = data.get('email')
        password = data.get('password')
        if None in (email, password):
            return "Parameters passed incorrectly", 400
        user = auth_service.create(data)
        if not user:
            return "User with this email is already registered", 400
        return "", 201, {"location": f'/auth/{user.id}'}


@auth_ns.route('/login')
class AuthView(Resource):
    def post(self):
        data = request.json

        email = data.get('email')
        password = data.get('password')
        if None in (email, password):
            return "", 400
        try:
            tokens = auth_service.generate_tokens(email, password)
            return tokens, 201
        except Exception:
            return "Invalid data entered"

    def put(self):
        tokens = request.json
        if None in (tokens["access_token"], tokens["refresh_token"]):
            return "", 400
        tokens = auth_service.approve_refresh_token(tokens)
        return tokens, 201


