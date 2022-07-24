from flask import request
from flask_restx import Namespace, Resource
from sqlalchemy import exc

from app.dao.model.movie import MovieSchema
from app.implemented import movie_service

movie_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        req_arg = request.args
        all_movies = movie_service.get_all(**req_arg)
        if all_movies:
            return movies_schema.dump(all_movies), 200
        return "Movies page is empty."


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid):
        try:
            movie = movie_service.get_one(mid)
            return movie_schema.dump(movie), 200
        except exc.NoResultFound:
            return 'A database result was required but none was found.'
