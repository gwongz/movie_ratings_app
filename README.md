Movie Ratings Application
======================

A Python application built using Flask and SQLAlchemy. The database is seeded with the [MovieLens](http://grouplens.org/datasets/movielens/) 100k dataset. It consists of 100,000 ratings of 1,700 movies from 1,000 users. 

Installation
------------
Step 1: Clone the repo 
`$git clone https://github.com/gwongz/movie_ratings_app.git`

Step 2: Create and activate a [virtualenv](http://www.virtualenv.org/en/latest/) inside your directory

Step 3: Install dependencies from the `requirements` file    

`$pip install -r requirements.txt`

Step 4: Run app in development web server and navigate to your localhost in your browser

`$python run.py`

`http://127.0.0.1:5000/`


Step 5: To run tests, navigate to the `/app` directory and run the `test` file from the command line

`$python test.py`