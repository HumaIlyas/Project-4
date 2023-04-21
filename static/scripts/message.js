// Set timeout function for the messages to disappear after some time
/* global bootstrap */

setTimeout(function () {
    let messages = document.getElementById("msg");
    let alert = new bootstrap.Alert(messages);
    alert.close();
}, 3000);