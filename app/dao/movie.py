from sqlalchemy import desc

from app.dao.model.director import Director
from app.dao.model.genre import Genre
from app.dao.model.movie import Movie


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self, **filters):
        movies = self.session.query(Movie.id, Movie.title, Movie.description, Movie.trailer,
                                    Movie.year, Movie.rating, Genre.name.label('genre'),
                                    Director.name.label('director')).join(Genre).join(Director)

        if 'status' in filters:
            if filters.get('status') == 'new':
                movies = movies.order_by(desc(Movie.year))

        if 'page' in filters:
            page_ = int(filters.get('page'))
            movies = movies.limit(12).offset(12*page_-12)

        return movies.all()

    def get_one(self, mid):
        movie = self.session.query(Movie.id, Movie.title, Movie.description, Movie.trailer,
                                   Movie.year, Movie.rating, Genre.name.label('genre'),
                                   Director.name.label('director')).join(Genre).join(Director)
        return movie.filter(Movie.id == mid).one()
