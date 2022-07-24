import base64
import hashlib
import hmac
import jwt


from app.dao.user import UserDAO
from app.helpers.constants import PWD_SALT, PWD_ITERATIONS, JWT_SECRET, JWT_ALGORITHM
from jwt.exceptions import InvalidSignatureError


class UserService:

    def __init__(self, dao: UserDAO):
        self.dao = dao

    def create(self, data):
        data['password'] = self.generate_password(data['password'])
        return self.dao.create(data)

    def update(self, token, data):
        user = self.get_user_by_tokens(token)
        if 'name' in data:
            user.name = data.get('name')
        if 'surname' in data:
            user.surname = data.get('surname')
        if 'favorite_genre' in data:
            user.favorite_genre = data.get('favorite_genre')
        return self.dao.patch(user)

    def update_password(self, token, old_password, new_password):
        user = self.get_user_by_tokens(token)
        real_str_user_password = user.password
        if not self.compare_passwords(real_str_user_password, old_password):
            return "Error"
        user.password = self.generate_password(new_password)
        return self.dao.update_password(user)

    def generate_password(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_SALT,
            PWD_ITERATIONS
        )
        return base64.b64encode(hash_digest)

    def get_by_user_email(self, email):
        return self.dao.get_by_user_email(email)

    def compare_passwords(self, password_hash, other_password) -> bool:
        decoded_digest = base64.b64decode(password_hash)
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            other_password.encode(),
            PWD_SALT,
            PWD_ITERATIONS
        )
        return hmac.compare_digest(decoded_digest, hash_digest)

    def get_user_by_tokens(self, tokens):
        if isinstance(tokens, str):
            try:
                data = jwt.decode(jwt=tokens, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
                email = data.get('email')
                return self.dao.get_by_user_email(email)
            except InvalidSignatureError:
                return None
        try:
            data = jwt.decode(jwt=tokens["access_token"], key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
            email = data.get('email')
            return self.dao.get_by_user_email(email)
        except InvalidSignatureError:
            try:
                data = jwt.decode(jwt=tokens["refresh_token"], key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
                email = data.get('email')
                return self.dao.get_by_user_email(email)
            except InvalidSignatureError:
                return None
