"""
Program 5: Implement user sessions in a Flask app to store and display user-specific data.
"""


from flask import Flask, render_template, redirect, session, request
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

@app.route("/")
def index():
    username = session.get("username", None)
    return render_template("username.html", username=username)


@app.route("/set_session", methods=["POST"])
def set_session():
    username = request.form.get("username")
    session['username'] = username
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8004)
