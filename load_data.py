import json

from app.dao.model.director import Director
from app.dao.model.genre import Genre
from app.dao.model.movie import Movie
from app.dao.model.user import User
from app.setup_db import db

with open('fixture.json', 'r') as f:
    fixture = json.load(f)


def all_data_load(data=fixture):
    for movie in data["movies"]:
        m = Movie(
            id=movie["pk"],
            title=movie["title"],
            description=movie["description"],
            trailer=movie["trailer"],
            year=movie["year"],
            rating=movie["rating"],
            genre_id=movie["genre_id"],
            director_id=movie["director_id"],
        )
        with db.session.begin():
            db.session.add(m)

    for director in data["directors"]:
        d = Director(
            id=director["pk"],
            name=director["name"],
        )
        with db.session.begin():
            db.session.add(d)

    for genre in data["genres"]:
        g = Genre(
            id=genre["pk"],
            name=genre["name"],
        )
        with db.session.begin():
            db.session.add(g)

    '''for user in data["users"]:
        u = User(
            id=user["pk"],
            email=user["email"],
            password=user["password"],
            name=user["name"],
            surname=user["surname"],
            favorite_genre=user["favorite_genre"]
        )
        with db.session.begin():
            db.session.add(u)

        ,
        "users": [
            {
                "pk": 1,
                "email": "asdasd",
                "password": "dsadsa",
                "name": "Тейлор Шеридан",
                "surname": "рпорп",
                "favorite_genre": "biba"
            }'''
