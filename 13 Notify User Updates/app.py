"""
Program 13: Design a Flask-socketio application for sending notifications to connected clients.

This Flask application integrates Flask and Flask-SocketIO to create a real-time notification system. It allows clients
to connect to the server and receive notifications sent by the server. Connected clients are stored in a set, and
notifications can be sent to all connected clients simultaneously.

The application includes the following components:
1. The main route ("/") renders an HTML template, "index.html," which serves as the main page for clients to receive
notifications.

2. Socket.IO event handlers:
   - "connect": Handles client connections, adds the client to the set of connected clients, and sends a connection
   message.
   - "disconnect": Handles client disconnections, removes the client from the set of connected clients, and sends a
   disconnection message.

3. A function, "notify_clients," that notifies all connected clients with a given message. It iterates over the set of
connected clients and sends the notification to each client individually.

4. A route ("/send_notification") to send notifications from the server to all connected clients. The server-side code
receives the message from the form and uses the "notify_clients" function to send the message to all connected clients.

To use the notification system:
1. Run the application using "socketio.run" with host "0.0.0.0" and the specified port.
2. Access the main page ("/") by navigating to the application's URL.
3. Clients can connect to the server and will receive notifications sent by the server.
4. Notifications can be sent from the server by submitting a message using the form provided.

This application demonstrates how Flask-SocketIO can be used to create real-time notification systems and provides a
simple example of real-time communication between the server and connected clients.

Note:
- Real-time notification systems are valuable for applications that require instant updates or notifications to
connected users.
- Connected clients are stored in a set to efficiently manage client connections and disconnections.
- The "notify_clients" function ensures that all connected clients receive the same message in real-time.
- Security and validation measures should be considered when implementing real-time communication features.
"""


from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)

app.config["SECRET_KEY"] = "shhh...secrett!!"
socketio = SocketIO(app)

# store connected clients in a set
connected_clients = set()

# route to render the main page
@app.route("/")
def index():
    return render_template("index.html")


# Socket.IO event handler for connecting a client
@socketio.on("connect")
def handle_connect():
    connected_clients.add(request.sid)
    emit("message", {"message": "Connected to the server."})


# Socket.IO event handler for disconnecting a client
@socketio.on("disconnect")
def handle_disconnect():
    connected_clients.remove(request.sid)
    emit("message", {"message": "Disconnected from the server."})


# notify all connected clients of updates
def notify_clients(message):
    for client in connected_clients:
        emit("notification", {"message": message}, room=client)


@app.route("/send_notification", methods=["POST"])
def send_notification():
    message = request.form.get("message")
    notify_clients(message)
    return "Notification Sent!"


if __name__ == "__main__":
    socketio.run(host="0.0.0.0", port=8013, debug=True, allow_unsafe_werkzeug=True, app=app)




