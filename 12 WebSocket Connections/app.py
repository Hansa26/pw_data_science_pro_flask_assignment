"""
Program 12: Design a Flask-socketio application for real-time data updates.

This Flask application integrates Flask and Flask-SocketIO to create a real-time data update application.
It continuously generates random temperature and humidity data and emits it to connected clients through a WebSocket,
allowing real-time visualization of data.

The application includes the following components:
1. The main route ("/") renders an HTML template, "index.html," which serves as the main page for data visualization.

2. A background task, "update_data," that generates random temperature and humidity data, emits it to connected clients,
 and updates the data every second. The background task ensures real-time data updates.

3. Socket.IO event handlers:
   - "connect": Handles client connections and logs a message when a client connects.
   - "disconnect": Handles client disconnections and logs a message when a client disconnects.

To test the real-time data update application:
1. Run the application using "socketio.run" with host "0.0.0.0" and the specified port.
2. Access the main page by navigating to the application's URL.
3. Connected clients will receive real-time temperature and humidity data updates.
4. Data updates will be visualized on the main page.

This application demonstrates how Flask-SocketIO can be used for real-time data streaming and its potential applications
 in real-time data visualization, monitoring, and more.

Note:
- Real-time applications are well-suited for scenarios where continuous data updates are required.
- The background task ensures data updates without blocking the main application.
- Proper usage of WebSocket technology and Flask-SocketIO enables real-time communication between the server and
connected clients.
- Consider security and data validation when implementing real-time data applications.
"""


from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random
import time


app = Flask(__name__)

app.config["SECRET_KEY"] = "shhh..secret!!"

socketio = SocketIO(app)

# route to render the main page
@app.route("/")
def index():
    return render_template("index.html")


# function to update data and emit it to connected clients
def update_data():
    while True:

        # generate some random data
        temperature = round(random.uniform(20.0, 30.0), 2)
        humidity = round(random.uniform(40.0, 60.0), 2)

        # emit the data to connected clients
        socketio.emit("update_data", {"temperature": temperature, "humidity": humidity})

        time.sleep(1)  # update data every 1 second


# Socket.IO event handler for connecting a client
@socketio.on("connect")
def handle_connect():
    print("Client connected")


# Socket.IO event handler for disconnecting a client
@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


if __name__ == "__main__":
    socketio.start_background_task(update_data)
    socketio.run(host="0.0.0.0", port=8012, debug=True, allow_unsafe_werkzeug=True, app=app)

