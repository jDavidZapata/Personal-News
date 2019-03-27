document.addEventListener('DOMContentLoaded', () => {

    // Template for roll results
    const comment_template = Handlebars.compile(document.querySelector('#comment').innerHTML);

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure button
    socket.on('connect', () => {
        
        const story_id = document.querySelector('.story-id').innerHTML;
        //const room = story_id

        // button should emit a "submit comment" event
        document.querySelector('#button').onclick =  () => {            
            
            const comment = document.querySelector('#comment-text').value;
            
            //const comment1 = document.createElement('div');
            //comment1.className = 'story-comment';
            //comment1.innerHTML = "#### New Comment###";
            //document.querySelector('#comments').append(comment1);
            socket.emit('submit comment', {'comment': comment, 'story_id': story_id});
        };
        
        // When page loads add user to room 
        socket.emit('join', {'room': story_id});

        

    });

    // When a new comment is announced, add to the div list
    socket.on('new comment', data => {
        add_comment(data)
        //document.querySelector('#new-comment').innerHTML = data.comment.comment_text;
        //document.querySelector('#user').innerHTML = data.comment.user.username;
    });

    console.log('DOM fully loaded and parsed');
    
    // Add lisener for unload event in order to take user out of room
    window.addEventListener('beforeunload', () => {
        const story_id = document.querySelector('.story-id').innerHTML;
        socket.emit('leave', {'room': story_id});
        console.log('DOM beforeunload');
    
    });
    
    // Add lisener for unload event in order to take user out of room
    window.addEventListener('unload', function(event) {
        const story_id = document.querySelector('.story-id').innerHTML;
        socket.emit('leave1', {'room': story_id});
        console.log('DOM on unloaded end');
    
  });

    // Add a new comment with given data to DOM.
    function add_comment(data) {

        // Create new comment.
        const comment = comment_template({'content1': "####", 'content2': data.user, 'content3': data.text});
        //const comment = document.createElement('div');
        //comment.className = 'story-comment';
        //comment.innerHTML = data;

        // Add comment to DOM.
        document.querySelector('#comments').innerHTML += comment;
        //document.querySelector('#comments').append(comment);

        // {messages.index(message) + 1} content1
        // {message.user.username} content2
        // {message.message_text} content3
    };




});



