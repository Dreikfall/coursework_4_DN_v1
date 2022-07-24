from sqlalchemy.exc import IntegrityError

from app.dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def create(self, data):
        try:
            user = User(**data)
            self.session.add(user)
            self.session.commit()
            return user
        except IntegrityError:
            return None

    def patch(self, user):
        self.session.add(user)
        self.session.commit()

    def update_password(self, user):
        self.session.add(user)
        self.session.commit()

    def get_by_user_email(self, email):
        user = self.session.query(User).filter(User.email == email).one_or_none()
        return user







