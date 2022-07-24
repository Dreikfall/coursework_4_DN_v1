from app.dao.director import DirectorDAO


class DirectorService:
    def __init__(self, dao: DirectorDAO):
        self.dao = dao

    def get_all(self, **filters):
        return self.dao.get_all(**filters)

    def get_one(self, did):
        return self.dao.get_one(did)
