from app.dao.model.director import Director


class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self, **filters):
        directors = self.session.query(Director)

        if 'page' in filters:
            page_ = int(filters.get('page'))
            directors = directors.limit(12).offset(12*page_-12)

        return directors.all()

    def get_one(self, did):
        director = self.session.query(Director).filter(Director.id == did).one()
        return director

