
from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from requests import delete
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError

from key import API_SECRET_KEY

from navigation import api_details, rate_multipler
from models import db, connect_db, User, Route 
from forms import LoginForm, RegisterForm, RouteForm, DeleteForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///routes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "NavigateForRate123$"

connect_db(app)
db.create_all()


@app.route("/")
def homepage():
    """Main Page (users will either register or sign in here"""

    return redirect("/register")



@app.route("/info")
def info_page():
    """Bring user to an information page that describes the application"""
    
    if "username" in session:

        return render_template("info.html")


##############################################################################
#routes related to user registration, login, & logout


@app.route("/register", methods=["GET", "POST"])
def register():
    """Allow user to sign in via a form"""

    if "username" in session:
        return redirect("/routes")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        company = form.company.data
        state = form.state.data

        user = User.register(username, password, first_name, last_name, company, state)

        db.session.commit()
        session["username"] = user.username
        flash("Account Created!")
        return redirect("/login")

    else:
        return render_template("register.html", form=form)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Handles user login"""

    if "username" in session:
        return redirect("/routes")


    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            flash("Welcome Back!")
            return redirect("/routes")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    """Logout the user"""

    if "username" not in session:
        return redirect("/login")
    
    session.pop("username")
    flash("Logged out.")
    return redirect("/login")

##############################################################################
#routes related to the functionality of the app

@app.route("/routes")
def show_user_routes():
    """Show a list of all user routes"""

    if "username" not in session:
        raise Unauthorized()

    if Route.query.all() is None:
        return redirect("/routes/add")


    routes = Route.query.all()

    return render_template("routes.html", routes=routes)


@app.route("/routes/<int:route_id>")
def show_route(route_id):
    """display a single route"""

    if "username" not in session:
        raise Unauthorized()

    route = Route.query.get_or_404(route_id)
    route.map_url = route.map_url.replace('API_SECRET_KEY', API_SECRET_KEY)

    payout = rate_multipler(route.mileage, route.travel_type)

    return render_template("route.html", route=route, payout=payout) 
    


@app.route("/routes/add", methods=["GET", "POST"])
def add_route():
    """Allow user to add a new route"""

    if "username" not in session:
        raise Unauthorized()

    username = session["username"]

    form = RouteForm()

    if form.validate_on_submit():
        start_point = form.start_point.data
        end_point = form.end_point.data
        travel_type = form.travel_type.data
        comments = form.comments.data

        distance = api_details(start_point, end_point)
        map_url = f"https://www.mapquestapi.com/staticmap/v5/map?key=API_SECRET_KEY&size=1100,500@2x&start={start_point}&end={end_point}"

        route = Route(username=username, start_point=start_point, end_point=end_point, travel_type=travel_type, mileage=distance, comments=comments, map_url=map_url)
        
        db.session.add(route)
        db.session.commit()
        flash("Route added.")

        return redirect("/routes")

    else:
        return render_template("new_route.html", form=form)


@app.route("/routes/<int:route_id>/delete", methods=["GET", "POST"])
def delete_route(route_id):
    """Delete a specific route"""

    if "username" not in session:
        raise Unauthorized()

    route = Route.query.get_or_404(route_id)
   
    db.session.delete(route)
    db.session.commit()

    flash("Route deleted.")

    return redirect("/routes")



