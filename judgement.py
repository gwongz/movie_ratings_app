from flask import Flask, render_template, redirect, request
import model

app = Flask (__name__)

@app.route("/")
def index():
    return render_template("index.html")
    # user_list = model.session.query(model.User).limit(5).all()
    # return render_template("user_list.html", user_list=user_list)
@app.route("/signup")
def signup():
    return render_template("signup.html")  

@app.route("/signin")
def get_user_by_id():
    u_id = request.args.get("ID")
    user = model.session.query(model.User).get(u_id)
    return render_template("user_info.html", user=user)

# @app.route("/user_home")
# def get_user_by_id():

#     id = request.args.get("id")
#     user_list = model.session.query(model.User).get(id)
#     return render_template("user_list.html", user_list=user_list)

@app.route("/add_user")
def add_user():
    user = model.User()
    user.email = request.args.get("email")
    user.password = request.args.get("password")
    user.occupation = request.args.get("occupation")
    user.age = request.args.get("age")
    user.zipcode = request.args.get("zipcode")
    user.gender = request.args.get("gender")

    model.session.add(user)
    model.session.commit()
   
    return render_template("user_info.html", user=user)

@app.route("/all_users")
def get_all_users():
    user_list = model.session.query(model.User).all()

    return render_template("user_list.html", user_list=user_list)

@app.route("/user_ratings")
def get_user_ratings():
    user_id = request.args.get("user_id")
    user = model.session.query(model.User).get(user_id)
   


 


    return render_template("user_ratings.html", user_id=user_id, ratings_list=user.ratings)

if __name__ == "__main__":
    app.run(debug = True)
