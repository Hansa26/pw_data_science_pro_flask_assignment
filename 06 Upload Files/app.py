"""
Program 6: Build a Flask app that allows users to upload files and display them on the website.
"""

from flask import Flask, flash, request, render_template, redirect, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configure the upload folder
UPLOAD_FOLDER = 'C:\\Users\\hansa\\OneDrive\\Documents\\Hansa-DataScience\\Python-Flask\\Assignment\\06 Upload Files\\uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    """
    Check if a filename has an allowed file extension.

    :param filename: (str) The name of the file to be checked.

    :returns: (bool) True if the file extension is in the list of allowed extensions; False otherwise.

    This function examines the provided filename to determine if it has an allowed file extension. It does so by checking
    if the filename contains a dot (.) and if the extension after the last dot is in the predefined list of allowed file
    extensions.
    """
    # Check if the filename contains a dot (.) and the extension after the last dot is in ALLOWED_EXTENSIONS.
    if '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
        return True
    else:
        return False


@app.route('/')
def index():
    """
    Render the homepage of the web application.

    :returns: An HTML page to be displayed to the user.

    Note:
    - The `@app.route('/')` decorator defines the route for the root URL of the application.
    - The `render_template` function is typically used to render HTML templates for web pages.
    """
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file uploads via HTTP POST request.

    :returns: A message indicating the result of the file upload.

    This function handles file uploads when a POST request is made to the '/upload' URL path. It checks if a file is included
    in the request and if the file has an allowed file extension using the 'allowed_file' function. If the conditions are met,
    the file is saved to the configured upload folder, and a success message is returned.

    Note:
    - The 'request' object is used to access data from the HTTP request.
    - The 'flash' function is used to display flash messages, typically used in web applications for notifications.
    - The 'secure_filename' function helps secure the filename when saving files.
    - The 'os.path.join' function is used to construct a safe file path for saving the uploaded file.

    """

    if request.method == "POST":
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Save the file to the uploads folder
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'File uploaded successfully'
        

@app.route('/files')
def list_files():
    """
    List and display files in the upload folder.

    :returns: An HTML page that displays the list of files in the upload folder.

    This function lists and displays files in the configured upload folder. It retrieves the list of files using the
    'os.listdir' function and passes this list to an HTML template for rendering.

    Note:
    - The 'os.listdir' function is used to retrieve the list of files in the upload folder.
    - The 'render_template' function is typically used to render HTML templates for web pages.
    """
    file_list = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('file_list.html', files=file_list)


@app.route('/display/<filename>')
def display_file(filename):
    """
    Serve a specific file for display.

    :param filename: (str) The name of the file to be served for display.

    :returns: File Response: The specified file to be displayed by the user's web browser.

    This function serves a specific file from the configured upload folder for download. It takes the filename as a parameter
    from the URL and sends the file to the user's web browser as a downloadable response.

    Note:
    - The 'send_from_directory' function is used to serve files from a specified directory.
    - The 'filename' parameter in the route URL is used to specify the name of the file to be served.
    - The user's web browser will prompt them to download the file.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8006, debug=True)


