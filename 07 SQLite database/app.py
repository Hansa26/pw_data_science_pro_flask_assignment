"""
Program 7: Integrate a SQLite database with Flask to perform CRUD operations on a list of items.

"""

from flask import Flask, render_template, redirect, request, url_for
import sqlite3

app = Flask(__name__)

# Database configuration
app.config["DATABASE"] = "database.db"

def get_db_connection():
    """
    Establish a connection to the SQLite database.

    :returns: sqlite3.Connection - A SQLite databse connection object with row factory enabled.

    This function establishes a connection to the SQLite database specified by the 'DATABASE' constant. It configures the
    connection to use the 'sqlite3.Row' row factory, which allows fetching rows as dictionaries, making it easier to work
    with query results.

    Note:
    - The 'DATABASE' constant should be defined elsewhere in the code to specify the path to the SQLite database file.
    - The row factory configuration enables fetching query results as dictionaries for easy data manipulation.

    """
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.execute("CREATE TABLE IF NOT EXISTS items ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    """
    Display a list of items from the database on the homepage.

    :returns: an HTML page displaying a list of items retrieved from the database

    This function is associated with the root URL of the web application. When a user accesses the root URL (e.g., "http://localhost:8007/"),
    this function is executed. It retrieves a list of items from the database and renders an HTML template to display those items on
    the homepage.

    Note:
    - The function uses the 'get_db_connection' function to establish a connection to the database.
    - It executes a SQL query to retrieve items from the database table 'items'.
    - The retrieved items are passed to the 'render_template' function to be displayed in the HTML template.
    - The database connection is closed after data retrieval.
    """
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('index.html', items=items)



@app.route("/add_item", methods=["POST"])
def add_item():
    """
    Add an item to the database.

    :returns: Redirect - A redirect to the 'index' route after successfully adding the item.

    This function is associated with the '/add_item' URL path and is designed to handle POST requests. It retrieves the name
    of an item from the request form and inserts it into the 'items' table in the database. After successfully adding the
    item, it redirects the user to the 'index' route.

    Note:
    - The function uses the 'get_db_connection' function to establish a connection to the database.
    - It retrieves the 'name' of the item from the request form.
    - An SQL query is executed to insert the item into the 'items' table.
    - The database connection is closed after the transaction is committed.
    - The user is redirected to the 'index' route, where the updated list of items is displayed.
    """
    if request.method == "POST":
        name = request.form["name"]
        conn = get_db_connection()
        conn.execute('INSERT INTO items (name) VALUES (?)', (name,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    

@app.route("/edit_item/<int:item_id>", methods=["POST", "GET"])
def edit_item(item_id):
    """
    View and edit information for a specific item.

    :param item_id: (int) The unique identifier of the item to be edited.

    :returns: Redirect or str: A redirect to the 'index' route after editing the item (POST), or an HTML page displaying item information and an edit form (GET).

    This function is associated with the '/edit_item/<item_id>' URL path, which takes an 'item_id' parameter. It is designed to handle both
    GET and POST requests. When a GET request is made, it retrieves the information for the specified item and renders an HTML template
    with an edit form. When a POST request is made, it updates the item's information in the database and redirects the user to the 'index' route.

    Note:
    - The function uses the 'get_db_connection' function to establish a connection to the database.
    - For GET requests, the item's information is retrieved and displayed with an edit form.
    - For POST requests, the item's information is updated in the database, and the user is redirected to the 'index' route.

    """
    conn = get_db_connection()
    item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    conn.close()

    if request.method == "POST":
        name = request.form["name"]
        conn = get_db_connection()
        conn.execute("UPDATE items SET name = ? WHERE id = ?", (name, item_id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    
    return render_template("edit.html", item=item)


@app.route("/delete_item/<int:item_id>")
def delete_item(item_id):
    """
    Delete a specific item from the database.

    :param item_id: (int) The unique identifier of the item to be deleted.

    :returns: Redirect - A redirect to the 'index' route after successfully deleting the item.

    This function is associated with the '/delete_item/<item_id>' URL path, which takes an 'item_id' parameter. When a GET request
    is made with a specific item's identifier, this function is executed. It deletes the specified item from the database and redirects
    the user to the 'index' route.

    Note:
    - The function uses the 'get_db_connection' function to establish a connection to the database.
    - An SQL query is executed to delete the item from the 'items' table based on the 'item_id' parameter.
    - The database connection is closed after the deletion is committed.
    - The user is redirected to the 'index' route, where the updated list of items is displayed.
    """
    conn = get_db_connection()
    conn.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8007, debug=True)