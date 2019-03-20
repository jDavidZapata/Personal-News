document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure button
    socket.on('connect', () => {

        // button should emit a "submit message" event
        document.querySelector('#button').onclick =  () => {            
            const channel_t = document.querySelector('.channel-title').innerHTML;
            const message = document.querySelector('#message-text').value;
            
            const message1 = document.createElement('div');
            message1.className = 'channel-message';
            message1.innerHTML = "#### new Message###";
            document.querySelector('#messages').append(message1);
            socket.emit('submit message', {'message': message, 'channel_t': channel_t});
        };
    });

    // When a new message is announced, add to the div list
    socket.on('new message', data => {
        add_message(data)
        //document.querySelector('#new-message').innerHTML = data.message.message_text;
        //document.querySelector('#user').innerHTML = data.message.user.username;
    });
});

// Add a new messaege with given data to DOM.
function add_message(data) {

    // Create new message.
    const message = document.createElement('div');
    message.className = 'channel-message';
    message.innerHTML = data;

    // Add message to DOM.
    document.querySelector('#messages').append(message);
};