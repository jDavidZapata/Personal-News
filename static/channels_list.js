document.addEventListener('DOMContentLoaded', () => {
    
    // Channel Room
    const room = 'channel_page_list';
    
    // Template for channel results
    const channel_template = Handlebars.compile(document.querySelector('#channel').innerHTML);
    
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure button
    socket.on('connect', () => {
            
        // When page loads add user to room 
        socket.emit('join', {'room': room});      

    });

    
    // When a new channel is announced, add to the div list
    socket.on('new channel', data => {
        add_channel(data)
        
    });

    console.log('DOM fully loaded and parsed');
    
    // Add lisener for unload event in order to take user out of room
    window.addEventListener('beforeunload', () => {
        
        socket.emit('leave', {'room': room});
        console.log('DOM beforeunload');
    
    });
    
    // Add lisener for unload event in order to take user out of room
    window.addEventListener('unload', function(event) {
        
        socket.emit('leave1', {'room': room});
        console.log('DOM on unloaded end');
    
    });

    
    // Add a new channel with given data to DOM.
    function add_channel(data) {

        // Create new channel.
        
        const channel = channel_template({'content1': `/channelPage/${data.title}`, 'content2': data.title, 'content3': data.user_name, 'content4': data.body});

        // Add channel to DOM.
        document.querySelector('#channels').innerHTML += channel;

    };


    
});

