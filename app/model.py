from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Date 
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session


# session object has query method; don't need connect function
# engine = create_engine("sqlite:///" + os.path.join(basedir, 'app.db')
engine = create_engine("sqlite:///app.db")
session = scoped_session(sessionmaker(bind=engine,
                                    autocommit = False,
                                    autoflush = False))

# class managed by SLALchemy

Base = declarative_base()
Base.query = session.query_property()

#inherits from Base 
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable = True)
    password = Column(String(64), nullable = True)
    age = Column(Integer, nullable = True)
    zipcode = Column(String(15), nullable = True)
    gender = Column(String(1))
    occupation = Column(String(64))

class Movie(Base):
    __tablename__= "movies"

    id = Column(Integer, primary_key = True)
    name = Column(String(64))
    released_at = Column(Date)
    imbd_url = Column(String(96))

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer)

    owner = relationship("User", backref = backref("ratings", order_by = id))
    movie = relationship("Movie", backref = backref("ratings", order_by = id))


#removed after threads introduced
# def connect():
#     global ENGINE
#     global Session

#     ENGINE = create_engine("sqlite:///ratings.db", echo=True)
#     Session = sessionmaker(bind=ENGINE)
#     return Session()

def init_db():
    Base.metadata.create_all(bind=engine)
 
def main():
    init_db()
    # Base.metadata.create_all(engine)

if __name__ == "__main__":
    main()
