"""
Program 10: Design a Flask app with proper error handling for 404 and 500 errors.

This Flask application demonstrates how to handle HTTP 404 (Not Found) and 500 (Internal Server Error) errors by defining custom error handlers. It includes routes that trigger these error conditions for testing purposes.

The application defines the following custom error handlers:
1. `page_not_found`: Handles the HTTP 404 error by rendering a custom "404.html" template and returning a 404 status code.
2. `internal_server_error`: Handles the HTTP 500 error (Internal Server Error) by rendering a custom "500.html" template and returning a 500 status code.

The application also includes two routes for testing:
1. `/notfound`: Triggers a 404 error by returning a custom message with a 404 status code.
2. `/servererror`: Triggers a 500 error by attempting to divide by zero (raising a ZeroDivisionError).

To test the error handling, access the `/notfound` and `/servererror` routes to see how the custom error pages are displayed when these errors occur.

Note:
- Error handlers are useful for providing user-friendly error pages and for gracefully handling errors in a Flask application.
- Custom error pages can be designed to match the application's style and branding.
- Proper error handling enhances the user experience and provides meaningful feedback in case of errors.

"""


from flask import Flask, render_template

app = Flask(__name__)

# define an error handler for 404 (Not Found) error
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# define an error handler for 500 (Internal Server Error) errors
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500

# a route that triggers a 404 error (for testing)
@app.route("/notfound")
def trigger_not_found():
    return "This page does not exist.", 404

# a route that triggers a 500 error (for testing)
@app.route("/servererror")
def trigger_server_error():
    a = 1/0 # this will raise a ZeroDivisionError and trigger a 500 error
    return "This should throw a 500 error, but you won't see this message."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8010, debug=True)
