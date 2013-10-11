from flask import Flask, render_template, redirect, request, session, g, url_for, flash, jsonify 
from model import session as db_session, User, Rating, Movie 

app = Flask(__name__)
app.secret_key = 'you-will-never-guess'


@app.route('/')
@app.route('/index')
def home():
    return render_template('login.html')

@app.before_request
def before_request():
    g.user_id = session.get('user_id')
    # g.user_id = session.get('user_id')
    # user_id = session.get("user_id")
    # if user_id:
    #     user = db_session.query(User).get(user_id)
    #     g.user = user
    # else:
    #     g.user = None

@app.teardown_request
def shutdown_session(exception = None):
    db_session.remove()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# def csrf_protect():
#     if request.method == 'POST':
#         token = session.pop('_csrf_token', None)
#         if not token or token != request.form.get('_csrf_token'):
#             abort(403)

# def generate_csrf_token():
#     if '_csrf_token' not in session:
#         session['_csrf_token'] = 'fdsldkfjde[qwbjwtv'
#     return session['_csrf_token']
# app.jinja_env.globals['csrf_token'] = generate_csrf_token

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
        return render_template('search.html', user=user) 

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    movies = db_session.query(Movie).filter(Movie.name.ilike('%' + query + '%')).limit(15).all()
    return render_template('results.html', movies=movies)
    
@app.route('/search', methods=['GET'])
def show_search():
    return render_template('search.html')

@app.route("/logout")
def logout():
    if not g.user_id:
    # if not g.user:
        return redirect(url_for('home'))  
    else:
        del session["user_id"] 
        flash('You have been logged out')
        return redirect(url_for('home'))

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    
    email= request.form["email"]
    password = request.form["password"]
    age = request.form["age"]
    gender = request.form["gender"]
    occupation = request.form["occupation"]
    zipcode = request.form["zipcode"]

    existing = db_session.query(User).filter_by(email=email).first()
    if existing:
        flash("I'm sorry. That email is already taken.")
        return redirect(url_for('signup')) 

    # elif not email or password or age or occupation or zipcode:
   
        # flash("Oops, looks like you didn't fill out the form completely.")
        # return render_template('signup.html')

    
    user = User(email=email, password=password, age=age, gender=gender, occupation=occupation, zipcode=zipcode)
    flash('Your account has been created.')
    db_session.add(user)
    db_session.commit()
    session['user_id'] = user.id
    return render_template("user.html", ratings=None)

@app.route('/movie/<int:id>', methods=['GET'])
def display_movie(id):

    movie = db_session.query(Movie).get(id)
    ratings = movie.ratings 
    total = []
    user_rating = None
    for rating in ratings:     
        if rating.user_id == session['user_id']:
            user_rating = rating
        total.append(rating.rating)
    avg_rating = float(sum(total))/len(total)

    # predict if no user rating
    prediction = None
    if not user_rating:
        user = db_session.query(User).get(g.user_id)
        prediction = user.predict_rating(movie)
        print "Prediction: ", prediction 

    return render_template('movie.html', movie=movie,
                            avg=avg_rating,
                            user_rating=user_rating,
                            prediction=prediction)

# @app.route("/movie", methods=['GET']) # display a movie's rating based on id
# def display_movie():
#     # try:
#     movie_id = int(request.args.get("id"))
#     movie = db_session.query(Movie).get(movie_id)
#     ratings = movie.ratings
#     user_rating = None
#     total = []
    
#     for r in ratings:
#         if r.rating == None:
#             continue   
#         if r.user_id == session['user_id']:
#             user_rating = r    
#         total.append(r.rating)
    
#     avg_rating = float(sum(total))/len(total)
#     print "This is avg rating", avg_rating

#     # check for prediction
#     user = db_session.query(User).get(session['user_id'])
#     print "User:", user 
#     prediction = None
#     print "prediction", prediction
#     if not user_rating:
#         prediction = user.predict_rating(movie)

#     # if not g.user: # if not logged in 
#         # return render_template('movie.html', movie=movie, 
#                                             # avg=avg_rating, 
#                                             # user_rating=False,
#                                             # prediction=False)

#     # else:
#     # for r in ratings:                
#     #     if r.user_id == session['user_id']:
#     #         user_rating = rating 
#     return render_template("movie.html", movie=movie, 
#                             avg=avg_rating, 
#                             user_rating=user_rating,
#                             prediction=prediction)

# except(TypeError):
    #     return redirect(url_for('search'))

@app.route("/rating", methods=['POST', 'GET'])
def rating():
    # try:
    user_id = session['user_id']

    value = request.form.get("rating")
    movie_id = request.form.get('movie_id')

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

    # except(KeyError):
    #     return redirect (url_for('search'))


@app.route('/user') # a user's movies
def user():
    if g.user_id == None:
        return render_template('login.html')
    else: 
        ratings = db_session.query(Rating).filter(Rating.user_id==g.user_id).all()
        return render_template('user.html', ratings=ratings)


@app.route('/all_movies')
def all_movies():
    movie_list = db_session.query(Movie).limit(30).all()
    return render_template('all_movies.html', movie_list=movie_list)

if __name__ == "__main__":
    app.run(debug = True)
