"""
Program 11: Design a Flask-socketio chat application for real-time communication.

This Flask application integrates Flask and Flask-SocketIO to create a real-time chat application. Users can connect,
exchange messages, and disconnect using WebSockets.

The application includes the following components:
1. The main route ("/") renders a chat interface using an HTML template "chat.html."

2. Socket.IO event handlers:
   - "connect": Handles user connections and logs a message when a user connects.
   - "disconnect": Handles user disconnections and logs a message when a user disconnects.
   - "message": Handles incoming chat messages, logs them, and emits the message to all connected clients for real-time
   chat.

To test the chat application:
1. Run the application using "socketio.run" with host "0.0.0.0" and the specified port.
2. Access the chat interface by navigating to the application's URL.
3. Users can connect and exchange messages in real-time through the chat interface.
4. Messages are broadcasted to all connected clients.

This application demonstrates the power of real-time communication using Flask-SocketIO and its ability to create
interactive chat applications.

Note:
- Proper usage of the WebSocket technology and Flask-SocketIO enables real-time, bidirectional communication between
clients and the server.
- Real-time applications can be extended for various purposes such as chat, gaming, notifications, and collaborative
tools.
- Security considerations should be taken into account when implementing real-time applications.
"""


from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)

app.config["SECRET_KEY"] = "shhhh..secret!"
socketio = SocketIO(app)


# route to render the chat interface
@app.route("/")
def chat():
    return render_template("chat.html")


# Socket.IO event handler for connecting a user
@socketio.on("connect")
def handle_connect():
    print("User Connected")


# Socket.IO event handler for disconnecting a user
@socketio.on("disconnect")
def handle_disconnect():
    print("User Disconnected")


@socketio.on("message")
def handle_message(message):
    print("Received Message: ", message)
    emit("message", message, broadcast=True)


if __name__ == "__main__":
    socketio.run(host="0.0.0.0", port=8011, app=app, debug=True, allow_unsafe_werkzeug=True)