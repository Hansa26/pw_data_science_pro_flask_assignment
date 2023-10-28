"""
Program 4: Create a Flask app with a form that accepts user input and displays it.
"""


from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


@app.route("/input")
def show_form():
    return render_template('input.html')



@app.route("/result", methods=["POST"])
def display_user_input():
    user_input = request.form.get("user_input")
    return render_template("output.html", user_input=user_input)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8003)
