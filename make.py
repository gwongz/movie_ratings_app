import model
from sqlalchemy.ext.declarative import declarative_base

ENGINE = None

def make(engine):
    Base.metadata.create_all(engine)

def main():
    global ENGINE
    ENGINE = create_engine("sqlite:///ratings.db", echo=True)
    make(ENGINE)

if __name__ == "__main__":
    main()