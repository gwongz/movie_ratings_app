from flask import Flask, render_template, redirect, request, session, g, url_for
import model

app = Flask (__name__)

app.secret_key = "abcdefghijklmnop"


@app.route("/")
def login():
    return render_template("index.html")

@app.route("/process_login", methods=["GET", "POST"])
def process_login():
    username = request.form.get("username")
    password = request.form.get("password")
    user = model.session.query(model.User).filter(model.User.email==username).filter(model.User.password==password).one()

    if not user:
        return redirect(url_for("login"))
    else:
        session['user_id'] = user.id
        return render_template("user_info.html", user=user)

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/add_user", methods=["POST"])
def add_user():
    user = model.User()
    user.email = request.form["email"]
    user.password = request.form["password"]
    user.age = request.form["age"]
    user.gender = request.form["gender"]
    user.occupation = request.form["occupation"]
    user.zipcode = request.form["zipcode"]

    model.session.add(user)
    model.session.commit()

    return render_template("user_info.html", user=user)

@app.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        user = model.session.query(model.User).get(user_id)
        g.user = user
    else:
        g.user = None

@app.route("/add_rating")
def add_rating():
    return render_template("add_rating.html")

@app.route("/new_rating", methods=["POST"])
def new_rating():
    new_rating = model.Rating()
    new_rating.user_id = g.user.id
    new_rating.rating = request.form["rating"]

    movie = model.session.query(model.Movie).filter(model.Movie.name == (request.form["name"])).first()
    if movie:
        new_rating.movie_id = movie.id
    else:
        movie = model.Movie()
        movie.name = request.form["name"]
        model.session.add(movie)
        model.session.commit()
        new_rating.movie_id = movie.id


    model.session.add(new_rating)
    model.session.commit()

    return render_template("user_info.html", user=g.user)

@app.route("/movies_by_user")
def get_movie_by_name_user():
    id = int(request.args.get("id"))
    movie = model.session.query(model.Movie).get(id)
    return "works!"

# @app.route("/all_movies")
# def all_movies():
#     # movies = model.session.query(model.Movie).all()
#     ratings = session.query(model.Ratings).all()
#     movies = session.query(model.Movies).all()
  



















# @app.route("/")
# def index():
#     return render_template("index.html")
#     # user_list = model.session.query(model.User).limit(5).all()
#     # return render_template("user_list.html", user_list=user_list)
# @app.route("/signup")
# def signup():
#     return render_template("signup.html")  

# @app.route("/signin")
# def get_user_by_id():
#     u_id = request.args.get("ID")
#     user = model.session.query(model.User).get(u_id)
#     return render_template("user_info.html", user=user)

# # @app.route("/user_home")
# # def get_user_by_id():

# #     id = request.args.get("id")
# #     user_list = model.session.query(model.User).get(id)
# #     return render_template("user_list.html", user_list=user_list)

# @app.route("/add_user")
# def add_user():
#     user = model.User()
#     user.email = request.args.get("email")
#     user.password = request.args.get("password")
#     user.occupation = request.args.get("occupation")
#     user.age = request.args.get("age")
#     user.zipcode = request.args.get("zipcode")
#     user.gender = request.args.get("gender")

#     model.session.add(user)
#     model.session.commit()
   
#     return render_template("user_info.html", user=user)

# @app.route("/all_users")
# def get_all_users():
#     user_list = model.session.query(model.User).all()

#     return render_template("user_list.html", user_list=user_list)

# @app.route("/user_ratings")
# def get_user_ratings():
#     user_id = request.args.get("user_id")
#     user = model.session.query(model.User).get(user_id)
   


 


#     return render_template("user_ratings.html", user_id=user_id, ratings_list=user.ratings)

if __name__ == "__main__":
    app.run(debug = True)
