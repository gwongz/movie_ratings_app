from flask import Flask, render_template, redirect, request, session, g, url_for, flash, jsonify 
from model import session as db_session, User, Rating, Movie 

app = Flask(__name__)
app.secret_key = "cant-guess-this"


@app.route("/hello")
def hello_username():
    return 'Hello %s' % request.form.get('username', 'nobody')


@app.route('/')
@app.route('/index')
def home():
    return render_template('login.html')

@app.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        user = db_session.query(User).get(user_id)
        g.user = user
    else:
        g.user = None

@app.route("/login", methods=['POST', 'GET'])
def login():
    username = request.form.get('username')
    password = request.form.get("password")
    user = db_session.query(User).filter(User.email==username).filter(User.password==password).first()

    if not user:
        flash('Invalid credentials')
        return render_template('login.html')
    
    else:
        session['user_id'] = user.id # scoped session
        flash('You were successfully logged in')
        return render_template('search.html', user=user) # change to search.html

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    print query 
    movies = db_session.query(Movie).filter(Movie.name.ilike('%' + query + '%')).limit(15).all()

    return render_template('results.html', movies=movies)
    
@app.route('/search', methods=['GET'])
def show_search():
    return render_template('search.html')

@app.route("/logout")
def logout():
    if session['user_id'] != None:
        del session["user_id"] 
        flash('You were logged out')

    return redirect(url_for('home'))


# POST 
@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    
    email = request.form["email"]
    password = request.form["password"]
    age = request.form["age"]
    gender = request.form["gender"]
    occupation = request.form["occupation"]
    zipcode = request.form["zipcode"]
    existing = db_session.query(User).filter_by(email=email).first()
    if existing:
        flash("I'm sorry. That email is already in use.")
        return redirect(url_for('home'))

    user = User(email=email, password=password, age=age, gender=gender, occupation=occupation, zipcode=zipcode)

    db_session.add(user)
    db_session.commit()

    session['user_id'] = user.id
    return render_template("user.html", user=user)

@app.route("/movie", methods=['GET']) # display a movie's rating based on id
def display_movie():
    movie_id = int(request.args.get("id"))
    movie = db_session.query(Movie).get(movie_id)
  
    ratings = movie.ratings
    user_rating = None
    total = []
    for rating in ratings:
        if rating.rating == None:
            continue       
        total.append(rating.rating)
    avg_rating = float(sum(total))/len(total)

    if not g.user: # if not logged in 
        return render_template('movie.html', movie=movie, avg=avg_rating, user_rating=False)

    else:
        for rating in ratings:                
            if rating.user_id == session['user_id']:
                user_rating = rating 
        return render_template("movie.html", movie=movie, avg=avg_rating, user_rating=user_rating)


@app.route("/rating")
def rating():

    user_id = session['user_id']
    value = request.args.get('rating')
    movie_id = request.args.get('movie_id')
    
    rating = db_session.query(Rating).filter(Rating.user_id==user_id).filter(Rating.movie_id==movie_id).first()

    if not rating:
        flash("Your rating has been added")
        rating = Rating()
        rating.user_id = user_id
        rating.movie_id = movie_id
        rating.rating = int(value)
        db_session.add(rating)
        db_session.commit()

   
    else:
        flash("Your rating has been updated")    
        rating.rating = int(value)
       
    db_session.commit()

    return redirect (url_for('display_movie', id=movie_id))


@app.route('/user') # a logged in user's movies
def user():
    if g.user == None:
        return render_template('login.html')
    else: 
        return render_template('user.html', user=g.user)

@app.route('/all_movies')
def all_movies():
    movie_list = db_session.query(Movie).limit(30).all()
    return render_template('all_movies.html', movie_list=movie_list)

if __name__=="__main__":
    app.run(debug = True)
