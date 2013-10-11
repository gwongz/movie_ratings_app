from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Date 
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

import correlation 


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

    def similarity(self, other):
        u_ratings = {}
        paired_ratings = []
        for r in self.ratings:
            u_ratings[r.movie_id] = r

        for r in other.ratings:
            u_r = u_ratings.get(r.movie_id)
            if u_r:
                paired_ratings.append( (u_r.rating, r.rating))

        if paired_ratings:
            return correlation.pearson(paired_ratings)
        else:
            return 0.0

    def predict_rating(self, movie):
        ratings = self.ratings 
        other_ratings = movie.ratings      
        similarities = [ (self.similarity(r.owner), r) for r in other_ratings ] 
        similarities.sort(reverse = True)
        similarities = [ sim for sim in similarities if sim[0] > 0 ]
        if not similarities:
            return None
        numerator = sum([ r.rating * similarity for similarity, r in similarities ])
        denominator = sum([ similarity[0] for similarity in similarities ])
        return numerator/denominator 


        # other_user_ids = [r.user_id for r in other_ratings]
        # other_users = []
        # for o_u in other_user_ids:
        #     user_obj = session.query(User).get(o_u)
        #     other_users.append(user_obj)
        # similarities = [ (user.similarity(other_user), other_user) \
        #     for r in other_ratings ]
        # similarities.sort(reverse = True)
        # top_user = similarities[0]
        # matched_rating = None
        # for rating in other_ratings:
        #     if rating.user_id == top_user[1].id: 
        #         matched_rating = rating
        #         break
        # return matched_rating.rating * top_user[0]


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

if __name__ == "__main__":
    main()
