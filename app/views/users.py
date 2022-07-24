from flask_restx import Namespace, Resource
from flask import request

from app.dao.model.user import UserSchema
from app.helpers.decorators import auth_required
from app.implemented import user_service

user_ns = Namespace('user')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@user_ns.route('/')
class UserView(Resource):
    @auth_required
    def get(self):
        data_head = request.headers["Authorization"]
        token = data_head.split('Bearer ')[-1]
        user = user_service.get_user_by_tokens(token)
        if user is None:
            return 'token(s) missing or decoding problem'
        return user_schema.dump(user), 200

    @auth_required
    def patch(self):
        data_head = request.headers["Authorization"]
        token = data_head.split('Bearer ')[-1]
        data_json = request.json
        user_service.update(token, data_json)
        return "", 204


@user_ns.route('/password')
class UserView(Resource):
    @auth_required
    def put(self):
        data_head = request.headers["Authorization"]
        token = data_head.split('Bearer ')[-1]
        data_json = request.json
        if None in (data_json['old_password'], data_json['new_password']):
            return "Password(s) not sent"
        if user_service.update_password(token, data_json['old_password'], data_json["new_password"]) == "Error":
            return "The old password was entered incorrectly", 400
        return "", 204


