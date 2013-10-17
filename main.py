from flask import Flask, render_template, redirect, request, session, g, url_for, flash
from model import session as db_session
from model import User, Rating, Movie 

app = Flask(__name__)
app.secret_key = 'you-will-never-guess'


@app.route('/')
@app.route('/index')
def home():
    return render_template('login.html')

@app.before_request
def before_request():
    g.user_id = session.get('user_id')

@app.teardown_request
def shutdown_session(exception = None):
    db_session.remove()

def redirect_url(default='home'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

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
        return redirect('user')
        # return render_template('search.html', user=user) 

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
    
    # try:
    email= request.form["email"]
    password = request.form["password"]
    age = request.form["age"]
    # gender = request.form["gender"]
    occupation = request.form["occupation"]
    zipcode = request.form["zipcode"]

    existing = db_session.query(User).filter(User.email==email).first()
    if existing:
        flash("I'm sorry. That email is already taken.")
        return redirect(url_for('signup')) 
    
    else:
        user = User(email=email, password=password, age=age, occupation=occupation, zipcode=zipcode)
        flash('Your account has been created.')
        db_session.add(user)
        db_session.commit()
        session['user_id'] = user.id
        return render_template("user.html", ratings=None)
    # except:
        # flash("It looks like there was an error with the form. Please fill out all fields.")
        # return redirect(url_for('signup'))
@app.route('/user')
def my_ratings():
    if not g.user_id:
        return redirect(url_for('home'))
    else:
        ratings = db_session.query(Rating).filter(Rating.user_id==g.user_id).all()
        return render_template('user.html', ratings=ratings)

@app.route('/movie/<int:id>', methods=['GET'])
def movie(id):
    if not g.user_id:
        print 'no global user'
        movie = db_session.query(Movie).get(id)
        ratings = movie.ratings
        total = []
        for rating in ratings:
            total.append(rating.rating)
        avg_rating = float(sum(total))/len(total)
        return render_template('movie.html', movie=movie,
                        avg=avg_rating, user_rating=None, prediction=None)

    else:

        movie = db_session.query(Movie).get(id)
        ratings = movie.ratings 
        total = []
        user_rating = None
        for rating in ratings:     
            if rating.user_id == g.user_id:
            # if rating.user_id == session['user_id']:
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


@app.route("/rating", methods=['POST', 'GET'])
def rating():

    if not g.user_id:
        flash("You have to be logged in to rate a movie.")
        id=request.args.get('/movie/=')
        print "This is the id", id 
        return redirect(redirect_url())
    else:

        user_id = session['user_id']
        value = int(request.form["rating"])
        movie_id = request.form['movie_id']
        rating = db_session.query(Rating).filter(Rating.user_id==user_id).filter(Rating.movie_id==movie_id).first()

        if not rating:
            flash("Your rating has been added")
            rating = Rating(user_id=user_id, movie_id=movie_id)
            # rating = Rating()
            # rating.user_id = user_id
            # rating.movie_id = movie_id
            # rating.rating = int(value)
            db_session.add(rating)
            # db_session.commit()

        else:
            flash("Your rating has been updated")    
            # rating.rating = int(value)
        rating.rating=value   
        db_session.commit()
        return redirect (url_for('movie', id=movie_id))


@app.route('/all_movies')
def all_movies():
    movie_list = db_session.query(Movie).limit(30).all()
    return render_template('all_movies.html', movie_list=movie_list)

if __name__ == "__main__":
    app.run(debug=True)
