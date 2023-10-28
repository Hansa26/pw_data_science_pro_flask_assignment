"""
Program 9: Create a RESTful API using Flask to perform CRUD(Create, Read, Update, Delete) operations on resources like
books or movies.

"""

from flask import Flask
from flask_restful import Api
from books import Books

app = Flask(__name__)
api = Api(app)

api.add_resource(Books, "/books", "/books/<int:book_id>")

if __name__ == "__main__":
    """
    Main entry point for the Flask RESTful API application.

    This script creates a Flask application and configures a RESTful API using Flask-RESTful.
    It maps the "Books" resource to the '/books' route, allowing access to a collection of books
    and individual book items.

    :returns:
    Starts the Flask application, making the RESTful API available for HTTP requests.

    Example Usage:
    - Run this script to start the Flask application.
    - Access the API endpoints at the specified URL (e.g., http://localhost:8009/books).

    Note:
    - The Flask application serves as a RESTful API for managing book information.
    - The "Books" resource handles CRUD (Create, Read, Update, Delete) operations on books.
    - The application runs in debug mode when executed directly (if __name__ == "__main__").
    - Make sure the "books" module contains the resource implementation.
    """
    app.run(host="0.0.0.0", port=8009, debug=True)

