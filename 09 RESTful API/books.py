from flask_restful import Resource, reqparse

books_data = [
    {
        "id": 1,
        "title": "Book 1",
        "author": "Author 1"
    },
    {
        "id": 2,
        "title": "Book 2",
        "author": "Author 2"
    }
]


class Books(Resource):

    """
    Resource class for managing a collection of books via a RESTful API.

    This class defines HTTP methods (GET, POST, PUT, DELETE) to handle book operations.
    It supports retrieving a list of books, adding a new book, updating an existing book,
    and deleting a book by its unique identifier.

    Methods:
    - get(self, book_id=None): Retrieve a list of books or a specific book by its ID.
    - post(self): Create a new book entry in the collection.
    - put(self, book_id): Update an existing book by its ID.
    - delete(self, book_id): Delete a book by its ID.

    :param book_id: (int, optional) The unique identifier of a book (default is None).

    :returns:
    - JSON response with book data or error message and HTTP status code.

    Usage:
    - Access the API endpoints for managing books.

    Note:
    - The resource relies on a data source named "books_data" (not shown here) for book storage.
    - It uses the Flask-RESTful RequestParser to handle input data.
    - HTTP status codes and JSON responses are used to communicate the results of operations.
    """

    def get(self, book_id=None):
        """
        Retrieve book(s) from the collection.

        This method handles HTTP GET requests to retrieve book entries from the collection of books.
        It can return either a specific book entry if a valid book_id is provided or the entire
        collection of books.

        :param book_id: (int, optional) The unique identifier of a book to retrieve.

        :return:
        - Tuple: A JSON response with book information and an HTTP status code (200 OK) if successful.
        - If a book with the provided book_id is not found, it returns a "Book not found" message and an HTTP status
        code (404 Not Found).

        Usage:
        - GET all books in the collection.
        - GET a specific book by providing its unique identifier (book_id).

        Note:
        - If book_id is provided, this method searches for a specific book by its unique identifier.
        - If book_id is not provided, this method returns the entire collection of books.
        """
        if book_id:
            book = next((
                book
                for book in books_data
                if book["id"] == book_id
            ), None)

            if book:
                return book, 200
            else:
                return "Book not found", 404

        return books_data, 200

    def post(self):
        """
        Create a new book entry in the collection.

        This method handles HTTP POST requests to add a new book to the collection of books. It expects
        a JSON payload with "title" and "author" fields to create a new book entry.

        Example Usage:
        - POST a new book entry to the API to add it to the collection.
        - Ensure the JSON payload contains "title" and "author" fields.

        Note:
        - This method uses the Flask-RESTful RequestParser to handle input data.
        - The "books_data" data source (not shown here) is updated with the new book entry.
        - An HTTP status code of 200 (OK) is returned upon successful creation.

        :return: - Tuple: A JSON response with the newly created book entry and an HTTP status code (200 OK).
        """
        parser = reqparse.RequestParser()
        parser.add_argument("title", type=str, required=True)
        parser.add_argument("author", type=str, required=True)
        args = parser.parse_args()

        new_id = max([book["id"] for book in books_data]) + 1
        args["id"] = new_id
        books_data.append(args)

        return args, 200

    def put(self, book_id):
        """
        Update a book in the collection.

        This method handles HTTP PUT requests to update a specific book entry in the collection of books.

        :param book_id: (int) The unique identifier of the book to update.

        :return:
        - Tuple: A JSON response with the updated book information and an HTTP status code (200 OK) if successful.
        - If the specified book_id does not exist in the collection, it returns a "Book not found" message and an HTTP
        status code (404 Not Found).

        Usage:
        - Update a specific book's title and author by providing its unique identifier (book_id).

        Note:
        - This method allows for the partial or complete update of a book's information, including its title and author.
        - If book_id is not found, it returns a "Book not found" message.
        """
        parser = reqparse.RequestParser()
        parser.add_argument("title", type=str)
        parser.add_argument("author", type=str)
        args = parser.parse_args()

        book = next((book for book in books_data if book["id"] == book_id), None)

        if book:
            book.update(args)
            return book, 200
        else:
            return "Book not found", 404

    def delete(self, book_id):
        """
        Delete a book from the collection.

        This method handles HTTP DELETE requests to remove a specific book entry from the collection of books.

        :param book_id: (int) The unique identifier of the book to be deleted.

        :return:
        - Tuple: A JSON response with a message indicating the successful deletion of the book and an HTTP status code
        (204 No Content).
        - If the specified book_id does not exist in the collection, it returns a "Book not found" message and an HTTP
        status code (404 Not Found).

        Usage:
        - Delete a specific book from the collection by providing its unique identifier (book_id).

        Note:
        - This method permanently removes a book from the collection.
        - If book_id is not found, it returns a "Book not found" message.
        """
        book = next((book for book in books_data if book["id"] == book_id), None)
        if book:
            books_data.remove(book)
            return "Book deleted", 204
        else:
            return "Book not found", 404



