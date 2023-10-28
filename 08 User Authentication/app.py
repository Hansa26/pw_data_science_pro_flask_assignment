"""
Program 8: Implement user authentication and registration in a Flask app using Flask-Login.

"""
# import the necessary modules.
from flask import Flask, redirect, url_for, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user

# create a flask application
app = Flask(__name__)

# tells flask-sqlalchemy what database to connect to
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

# Enter the secret key
app.config["SECRET_KEY"] = "hsggg"

# Initialize flask-sqlalchemy extension
db = SQLAlchemy()

# LoginManager is needed for our application to be able to login and logout users
login_manager = LoginManager()
login_manager.init_app(app)


# create a user model
class Users(UserMixin, db.Model):
    """
    Represents a user in the application.

    This class defines the structure of the Users table in the database. Each user has a unique ID, a username,
    and a password. UserMixin is included to provide default user-related methods and properties.

    :attributes:
    - id (int): The unique identifier for the user.
    - username (str): The username of the user. It must be unique and is required.
    - password (str): The password associated with the user. It is required for authentication.

    Usage:
    You can use this class to interact with user data in the application, such as creating, retrieving, and managing
    user records.

    Note:
    This class should be used in conjunction with a database (e.g., SQLAlchemy) to persist user data.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


# initialize app with extension
db.init_app(app)

# create database within app context
with app.app_context():
    db.create_all()


# creates a user loader callback that returns the user object given an id
@login_manager.user_loader
def loader_user(user_id):
    """
    Load a user from the database based on the user's ID.

    This function is used as a user loader by Flask-Login. It retrieves a user object from the database
    based on the user's unique ID.

    :param user_id: The unique identifier (ID) of the user to be loaded.

    :return: A user object that corresponds to the given user ID.

    This function is typically used with Flask-Login's user management to authenticate and manage user sessions.
    When a user logs in, Flask-Login uses this function to load the user object from the database based on the user's
    ID.

    Note:
    Make sure that you have properly configured Flask-Login and that the 'Users' model represents user data and is
    set up with SQLAlchemy.

    """
    return Users.query.get(user_id)


@app.route("/register", methods=["POST", "GET"])
def register():
    """
    Register a new user by processing a registration form.

    This route handles both GET and POST requests. If the request method is POST,
    it processes the submitted registration form, creating a new user account and
    adding it to the database. If the method is GET, it displays the registration form
    for the user to fill in.

    :returns:
    - For GET requests: Renders the 'sign_up.html' template to display the registration form.
    - For POST requests: Redirects the user to the login route after successfully creating

    Usage:
    To register a new user, the user accesses the '/register' route, fills in the registration form,
    and submits it. The new user account is created, and they are redirected to the login page.

    Note:
    This route assumes that the database (db) and the 'Users' model have been correctly configured
    for user registration and account storage.
    """

    # if the user made a POST request, create a new user
    if request.method == "POST":
        user = Users(username=request.form.get("username"), password=request.form.get("password"))

        # add the user to the database
        db.session.add(user)

        # commit the changes made
        db.session.commit()

        # once the user account is created, redirect them to login route.
        return redirect(url_for("login"))

    # renders sign_up template if user made a GET request
    return render_template("sign_up.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    """
    Handle user authentication for logging in.

    This route supports both GET and POST requests. For POST requests, it attempts to authenticate
    the user based on the provided username and password. If successful, the user is logged in
    using the `login_user` method, and they are redirected to the home route. If the password is
    incorrect or the user doesn't exist, appropriate error messages are flashed to the user.

    :returns:
    - For GET requests: Renders the 'login.html' template to display the login form.
    - For POST requests: Redirects the user to the home route if authentication is successful,
      or flashes error messages and redirects to the home route in case of authentication failure.

    Usage:
    - A user accesses the '/login' route, fills in the login form, and submits it to log in.
    - If authentication is successful, the user is redirected to the home page.
    - If the entered password is incorrect or the user doesn't exist, appropriate error messages
      are displayed and the user is redirected to the home page.

    Note:
    This route assumes that the database (db) and the 'Users' model have been correctly configured
    for user authentication.
    """

    # is a post request is made, find the user by filtering for username

    if request.method == "POST":
        user = Users.query.filter_by(username=request.form.get("username")).first()

        try:
            # check if the password entered is the same as user's password
            if user.password == request.form["password"]:
                # use the login_user method to log in the user
                login_user(user)

                # redirect the user back to the home.
                return redirect(url_for("home"))
            else:
                flash("Password is Incorrect!")
                return redirect(url_for("home"))
        except Exception as ex:
            flash("You are not a registered user. Please login.")
            return redirect(url_for("home"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    """
    Handle user logout.

    This route logs out the currently authenticated user using the `logout_user` method from
    Flask-Login and redirects them to the home page after successfully logging out.

    :return: Redirects the user to the home route (typically the login page after logout).

    """
    logout_user()
    return redirect(url_for("home"))


@app.route("/")
def home():
    """
    Render the home page.

    This route renders the 'home.html' template, which typically serves as the landing page or
    main page of the application.

    :return: Renders the 'home.html' template for user interaction.
    """

    # render home.html on "/" route
    return render_template("home.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8008, debug=True)
