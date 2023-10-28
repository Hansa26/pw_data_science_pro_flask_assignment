document.addEventListener('DOMContentLoaded', function () {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    // Event handler for receiving and displaying data updates
    socket.on('update_data', function (data) {
        $('#temperature').text(data.temperature);
        $('#humidity').text(data.humidity);
    });
});
