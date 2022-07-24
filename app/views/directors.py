from flask import request
from flask_restx import Namespace, Resource
from sqlalchemy import exc

from app.dao.model.director import DirectorSchema
from app.implemented import director_service

director_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        req_arg = request.args
        all_directors = director_service.get_all(**req_arg)
        if all_directors:
            return directors_schema.dump(all_directors), 200
        return "Directors page is empty."


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did):
        try:
            director = director_service.get_one(did)
            return director_schema.dump(director), 200
        except exc.NoResultFound:
            return 'A database result was required but none was found.'
