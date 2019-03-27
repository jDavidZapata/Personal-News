document.addEventListener('DOMContentLoaded', () => {

    // Template for roll results
    const message_template = Handlebars.compile(document.querySelector('#message').innerHTML);

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure button
    socket.on('connect', () => {
        
        const channel_t = document.querySelector('.channel-title').innerHTML;

        // button should emit a "submit message" event
        document.querySelector('#button').onclick =  () => {            
            
            const message = document.querySelector('#message-text').value;
            
            socket.emit('submit message', {'message': message, 'channel_t': channel_t});
        };
        
        // When page loads add user to room 
        socket.emit('join', {'room': channel_t});      

    });

    // When a new message is announced, add to the div list
    socket.on('new message', data => {
        add_message(data)
        
    });

    console.log('DOM fully loaded and parsed');
    
    // Add lisener for unload event in order to take user out of room
    window.addEventListener('beforeunload', () => {
        const channel_t = document.querySelector('.channel-title').innerHTML;
        socket.emit('leave', {'room': channel_t});
        console.log('DOM beforeunload');
    
    });
    
    // Add lisener for unload event in order to take user out of room
    window.addEventListener('unload', function(event) {
        const channel_t = document.querySelector('.channel-title').innerHTML;
        socket.emit('leave1', {'room': channel_t});
        console.log('DOM on unloaded end');
    
    });

    
    // Add a new messaege with given data to DOM.
    function add_message(data) {

        // Create new message.
        var messages_list = document.querySelectorAll('.channel-message').length;
        const message = message_template({'content1': messages_list + 1, 'content2': data.user, 'content3': data.text});

        // Add message to DOM.
        document.querySelector('#messages').innerHTML += message;

    };

    
});



