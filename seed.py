import model
import csv
from sqlalchemy import Date
import datetime
import re


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
        movie_info = csv.reader(csvfile, delimiter = '|', quotechar = " ")
        for row in movie_info:
            old_date = row[2]
            try:
                new_date = datetime.datetime.strptime(old_date, '%d-%b-%Y')
            except ValueError:
                continue 
            final_date = new_date.strftime('%Y,%m,%d')
            f = final_date.split(',')

            name = row[1]
            name= name.decode("latin-1")
            name_2 = re.sub("[(\d+)]", "", name)
            name_2 = name_2.strip()
            
            movie = model.Movie(id = row[0],
                                name = name_2,
                                released_at = (datetime.date(int(f[0]),int(f[1]),int(f[2]))),
                                imbd_url = row[4])
            session.add(movie)
        session.commit()

 
    

def load_ratings(session):
    with open ('seed_data/u.data') as csvfile:
        ratings_info = csv.reader(csvfile, delimiter = "\t")
        for row in ratings_info:
            rating = model.Rating(user_id = row[0],
                                movie_id = row[1],
                                rating = row[2])
            session.add(rating)
        session.commit()

        

    

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    session = model.connect()
    load_users(session)
    load_movies(session)
    load_ratings(session)

if __name__ == "__main__":
    s= model.connect()
    main(s)
