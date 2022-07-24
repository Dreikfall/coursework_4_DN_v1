import calendar
import datetime
import jwt
from jwt.exceptions import DecodeError

from flask_restx import abort

from app.helpers.constants import JWT_SECRET, JWT_ALGORITHM
from app.services.user import UserService


class AuthService:
    def __init__(self, user_serv: UserService):
        self.user_serv = user_serv

    def create(self, data):
        return self.user_serv.create(data)

    def generate_tokens(self, email, password, is_tokens=False):
        """Функция генерации токенов"""
        user = self.user_serv.get_by_user_email(email)
        if user is None:
            raise abort(404)
        if not is_tokens:
            if not self.user_serv.compare_passwords(user.password, password):
                abort(400)
        data = {
            'email': user.email
        }
        # 30 minutes for acces token
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        # 100 days for refresh_token
        days100 = datetime.datetime.utcnow() + datetime.timedelta(days=100)
        data['exp'] = calendar.timegm(days100.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def approve_refresh_token(self, tokens):
        """Генерация новых токенов из валидных токенов"""
        try:
            data = jwt.decode(jwt=tokens["access_token"], key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
            email = data.get('email')
            return self.generate_tokens(email, None, is_tokens=True)
        except DecodeError:
            try:
                data = jwt.decode(jwt=tokens["refresh_token"], key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
                email = data.get('email')
                return self.generate_tokens(email, None, is_tokens=True)
            except Exception:
                return "tokens have not been validated"



