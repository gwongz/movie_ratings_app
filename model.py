from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date 
from sqlalchemy.orm import sessionmaker


ENGINE = None
Session = None

Base = declarative_base()

### Class declarations go here

#This class = User table and inherits from Base in SQLALCHEMY
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable = True)
    password = Column(String(64), nullable = True)
    age = Column(Integer, nullable = True)
    zipcode = Column(String(15), nullable = True)
    gender = Column(String(1))
    occupation = Column(String(64))

    #   We don't need Init in our classes 
    # def __init__(self, id, age, zipcode, email = None, password = None):     
    #     self.email = email
    #     self.password = password
    #     self.age = age
    #     self.zipcode = zipcode


#This class = Movie table and inherits from Base in SQLALCHEMY
class Movie(Base):
    __tablename__= "movies"

    id = Column(Integer, primary_key = True)
    name = Column(String(64))
    released_at = Column(Date)
    imbd_url = Column(String(96))


    #   We don't need Init in our classes 
    # def __init__(self, name, released_at, imbd_url):  
    #     self.name = name
    #     self.released_at = released_at
    #     self.imbd_url = imbd_url



#This class = Ratings table and inherits from Base in SQLALCHEMY
class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer)
    user_id = Column(Integer)
    rating = Column(Integer)


    #   We don't need Init in our classes 

    # def __init__(self, movie_id, user_id, rating):
    #     self.movie_id = movie_id
    #     self.user_id = user_id
    #     self.rating = rating

### End class declarations
def connect():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///ratings.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return Session()

def main():
    pass

if __name__ == "__main__":
    main()


