from py2neo.ogm import GraphObject, Property,RelatedFrom, RelatedTo, Model, Repository
from appl.app import login_manager,url,username
from datetime import datetime
repo = Repository(url)



@login_manager.user_loader
def load_user(email):
    print(repo.match(User, email).first())
    return repo.match(User, email).first()


class Movie(Model):
    __primarykey__ = "show_id"
    title = Property()
    show_id = Property()
    type = Property()
    country = Property()
    release_year = Property()
    description = Property()
    director = Property()
    cast = Property()
    genre = Property()
    rated = RelatedFrom("Rated", "Genre_IN")




class User(GraphObject):
    __primarylabel__ = "user"
    __primarykey__ = "email"
    id = Property()
    name = Property()
    email = Property()
    password = Property()
    hashed_password = Property()
    last_login = Property()
    rated_in = RelatedTo(Movie)

    def __init__(self, name):
        self.name = name
        self.last_login = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        print(self.email)
        return self.email

    def find(self):
        user = repo.match(User, self.email).first()
        return user


class Actor(Model):
    __primarykey__ = "name"
    name = Property()
    acted_in = RelatedTo(Movie)


class Director(GraphObject):
    __primarykey__ = "name"

    name = Property()
    directed = RelatedTo(Movie)


class Genre(GraphObject):
    __primarykey__ = "name"

    name = Property()

    genre_in = RelatedTo(Movie)