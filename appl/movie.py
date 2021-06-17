from appl.app import graph
from typing import Optional
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from appl.models import Actor,Movie,Genre,Director,repo
import pandas as pd


def create_movie():
    fas = Movie()
    fas.title = "as"
    graph.create(fas)
    alice = Actor()
    alice.name = "Alice Smith"
    alice.acted_in.add(fas)
    graph.create(alice)
    d = Movie()
    d.title = "ddsa"
    graph.create(d)


def add_movie():
    exel_data =pd.read_excel('qwert.xlsx',sheet_name='movie')
    excel_data_df = pd.read_excel('qwert.xlsx', sheet_name='movie', usecols=exel_data.columns)
    for el in excel_data_df.to_dict(orient='record'):
        movie = Movie()
        print(el['show_id'])
        movie.title = el['title']
        movie.show_id = el['show_id']
        movie.type = el['type']
        movie.country = el['country']
        movie.cast = el['cast']
        movie.description = el['description']
        movie.release_year = el['release_year']
        movie.director = el['director']
        movie.genre = el['listed_in']
        graph.create(movie)
        if type(movie.cast) != float:
            i = 0
            for ac in movie.cast.split(', '):
                if i == 3:
                    break
                i+=1
                acto = repo.match(Actor, ac).first()
                if acto != None:
                    acto.acted_in.add(movie)
                    graph.push(acto)
                else:
                    actor = Actor()
                    actor.name = ac
                    actor.acted_in.add(movie)
                    graph.create(actor)
        director = repo.match(Director, movie.director).first()
        if director != None:
            director.directed.add(movie)
            graph.push(director)
        else:
            director = Director()
            director.name = movie.director
            director.directed.add(movie)
            graph.create(director)
        for ac in el['listed_in'].split(', '):
            genre = repo.match(Genre, ac).first()
            if genre != None:
                genre.genre_in.add(movie)
                graph.push(genre)
            else:
                genre = Genre()
                genre.name = ac
                genre.genre_in.add(movie)
                graph.create(genre)