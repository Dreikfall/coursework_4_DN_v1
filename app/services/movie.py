from app.dao.movie import MovieDAO


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_all(self, **filters):
        return self.dao.get_all(**filters)

    def get_one(self, mid):
        return self.dao.get_one(mid)
