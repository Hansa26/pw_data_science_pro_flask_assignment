document.addEventListener('DOMContentLoaded', function () {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    // Send a message to the server
    $('#send_button').click(function () {
        socket.emit('message', $('#message_input').val());
        $('#message_input').val('');
    });

    // Receive and display messages from the server
    socket.on('message', function (message) {
        $('#messages').append($('<li>').text(message));
    });

    // Handle user disconnect
    socket.on('disconnect', function () {
        console.log('Disconnected from the server');
    });
});
