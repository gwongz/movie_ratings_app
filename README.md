Movie Ratings Application
=========================

This is a movie rating system based on machine learning principles. Using the Pearson Correlation, it determines how similar users in the database are to each other and predicts how a user will rate a movie. The database is seeded with the [MovieLens](http://grouplens.org/datasets/movielens/) 100k dataset. It consists of 100,000 ratings of 1,700 movies from 1,000 users. 

Watch a [screencast](http://youtu.be/Fjqc8EISZUA)


Installation
------------
Step 1: Clone the repo     
`$ git clone https://github.com/gwongz/movie_ratings_app.git`

Step 2: Create and activate a [virtualenv](http://www.virtualenv.org/en/latest/) inside your directory

Step 3: Install dependencies from the `requirements` file        
`$ pip install -r requirements.txt`

Step 4: Run the `main` file in the development web server and navigate to localhost in your browser   
`$ python main.py`        
`http://127.0.0.1:5000/`


Step 5: To run tests on the app, run the `test` file from the command line     
`$ python test.py`

![Alt text](/screenshots/login.png "Screenshot of login page")
![Alt text](/screenshots/prediction.png "Screenshot of predicted rating")
![Alt text](/screenshots/user_ratings.png "Screenshot of user's ratings")