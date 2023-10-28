"""
Program 3: Develop a Flask app that uses URL parameters to display dynamic content.
"""


from flask import Flask, request

app = Flask(__name__)


@app.route("/urlparams")
def get_url_parameters():
    name = request.args.get("name")
    age = request.args.get("age")
    
    return f"Hi, My name is {name}, and I am {age} years old!"



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002)
