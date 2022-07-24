from app.dao.model.genre import Genre


class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self, **filters):
        genres = self.session.query(Genre)

        if 'page' in filters:
            page_ = int(filters.get('page'))
            genres = genres.limit(12).offset(12*page_-12)

        return genres.all()

    def get_one(self, gid):
        genre = self.session.query(Genre).filter(Genre.id == gid).one()
        return genre
