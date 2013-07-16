import model
import csv
from sqlalchemy import Date
import datetime


def load_users(session):
    with open ('seed_data/u.user') as csvfile:
        user_info = csv.reader(csvfile, delimiter ='|')
        for row in user_info:
            user = model.User(id = row[0], 
                            age = row[1], 
                            gender = row[2], 
                            occupation = row[3],
                            zipcode = row[4])
            session.add(user)
        session.commit()

def load_movies(session):
    with open ('seed_data/u.item') as csvfile:
        movie_info = csv.reader(csvfile, delimiter = '|', quotechar = " " )
        for row in movie_info:
            movie = model.Movie(id = row[0],
                                name = row[1],
                                released_at = int(datetime.date(row[2])),
                                imbd_url = row[4])
            session.add(movie)
        session.commit()

    # use u.item
    

def load_ratings(session):
    # use u.data
    pass

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    session = model.connect()
    # load_users(session)
    load_movies(session)
    # load_ratings(session)

if __name__ == "__main__":
    s= model.connect()
    main(s)
