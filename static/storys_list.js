document.addEventListener('DOMContentLoaded', () => {
    
    // Channel Room
    const room = 'story_page_list';
    
    // Template for story results
    const story_template = Handlebars.compile(document.querySelector('#story').innerHTML);
    
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure button
    socket.on('connect', () => {
            
        // When page loads add user to room 
        socket.emit('join', {'room': room});      

    });

    
    // When a new story is announced, add to the div list
    socket.on('new story', data => {
        add_story(data)
        
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

    
    // Add a new story with given data to DOM.
    function add_story(data) {

        // Create new story.
        
        const story = story_template({'content1': `/storyPage/${data.story_id}`, 'content2': data.title, 'content3': data.user_name, 'content4': data.body});

        // Add story to DOM.
        document.querySelector('#storys').innerHTML += story;

    };


    
});

