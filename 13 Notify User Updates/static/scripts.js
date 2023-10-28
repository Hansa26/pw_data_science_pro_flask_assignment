document.addEventListener('DOMContentLoaded', function () {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    // Event handler for receiving and displaying notifications
    socket.on('notification', function (data) {
        $('#notifications').append($('<p>').text(data.message));
    });
});
