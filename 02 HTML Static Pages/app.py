"""
Program 2: Build a Flask app with static HTML pages and navigate between them.
"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/home")
def show_main_page():
    return render_template('index.html')


@app.route("/page1")
def show_page1():
    return render_template('page1.html')

@app.route("/page2")
def show_page2():
    return render_template('page2.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)