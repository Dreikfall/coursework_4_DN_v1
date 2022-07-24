from flask import request
from flask_restx import Namespace, Resource
from sqlalchemy import exc

from app.dao.model.genre import GenreSchema
from app.implemented import genre_service

genre_ns = Namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        req_arg = request.args
        all_genres = genre_service.get_all(**req_arg)
        if all_genres:
            return genres_schema.dump(all_genres), 200
        return "Genres page is empty."


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid):
        try:
            genre = genre_service.get_one(gid)
            return genre_schema.dump(genre), 200
        except exc.NoResultFound:
            return 'A database result was required but none was found.'
