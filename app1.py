from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def index():

	return render_template("index.html")

texts = ["Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam tortor mauris, maximus semper volutpat vitae, varius placerat dui. Nunc consequat dictum est, at vestibulum est hendrerit at. Mauris suscipit neque ultrices nisl interdum accumsan. Sed euismod, ligula eget tristique semper, lectus est pellentesque dui, sit amet rhoncus leo mi nec orci. Curabitur hendrerit, est in ultricies interdum, lacus lacus aliquam mauris, vel vestibulum magna nisl id arcu. Cras luctus tellus ac convallis venenatis. Cras consequat tempor tincidunt. Proin ultricies purus mauris, non tempor turpis mollis id. Nam iaculis risus mauris, quis ornare neque semper vel.",
		"Praesent euismod auctor quam, id congue tellus malesuada vitae. Ut sed lacinia quam. Sed vitae mattis metus, vel gravida ante. Praesent tincidunt nulla non sapien tincidunt, vitae semper diam faucibus. Nulla venenatis tincidunt efficitur. Integer justo nunc, egestas eget dignissim dignissim, fermentum ac sapien. Suspendisse non libero facilisis, dictum nunc ut, tincidunt diam.",
		"Morbi imperdiet nunc ac quam hendrerit faucibus. Morbi viverra justo est, ut bibendum lacus vehicula at. Fusce eget risus arcu. Quisque dictum porttitor nisl, eget condimentum leo mollis sed. Proin justo nisl, lacinia id erat in, suscipit ultrices nisi. Suspendisse placerat nulla at volutpat interdum. In porttitor condimentum est nec ultricies. Donec nec mollis neque, id dapibus sem.",
		"Home", "Caterory", "Create Category", "Create Channel", "Log Out", "Log In", "Register", "Channel Page", "Story Page", "List of News Links", "list of categories", "category:[happy,romantic,sad]", "'channel list':['Channel1', 'channel2', 'channel3', 'channel4', 'channel5']"]


@app.route("/home")
def home():

	# Api call for links to news site.
	# Send list News links. 
	#  return jsonify(f"{texts[3]} =======>>>>    {texts[0]}")

	return jsonify(texts[3], texts[12])




@app.route("/category")
def category():

	#Send a list of links to categories.
	#if 
	#return jsonify(texts[4], texts[13], texts[14])

	return render_template("category.html")


@app.route("/createCategory")
def createCategory():

	#Display Form for creating Categories.
	#If Post then take form info and create category.
	#If it already exists send list of stories.
	#If it doesnt exist then send "Create or add a story" 


	return jsonify(texts[5])

@app.route("/createChannel")
def createChannel():

	#Display Form for creating Channel.
	#Only one channel per user.
	#If Post then take form info and create Channel.
	#If it already exists send "Channel already taken."
	#If it doesnt exist then, send 
	#"Create or add a story to Your channel".
	#And send a list of categories.
	
	return jsonify(texts[6])

@app.route("/logout")
def logout():

	#Log out user from session on server.
	#Send list of News links'''
	#return jsonify(texts[7])
	return render_template("index.html")


@app.route("/login")
def login():

	#Display Form for Loging in user.
	#If Post check to make sure user exists.
	#If no User send "User doesnt exist."
	#Else Log In user to session on server.
	#Send back last place user was when loged out. 
	
	return jsonify(texts[8])

@app.route("/register")
def register():

	#Display Form for Registration.
	#If Post Register User and add to database.
	#Send back list of news links. '''

	return jsonify(texts[9])


@app.route("/channelPage")
def channelPage():

	#Send back list of news links on channel.
	#Send back first 100 messages.
	#Send back Form for messages.(JS)
	#return jsonify(texts[10])

	channel = {"title":"My Channel", "author":"Juan David", "year": 2019, "text": "This is My Channel."}
	storys = [{"title": "A story", "text": "this is my first story."},{"title": "Another story", "text": "this is my second story."} ]
	messages = [{"text":"hello, 1st message"}, {"text":"world, 2nd message"}, {"text":"And this is the 3rd message."}]

	return render_template("channel_page.html", storys=storys, messages=messages)


@app.route("/storyPage")
def storyPage():	

	# Display Story.
	#	Send back Story text.
	#	Send back first 100 comments.
	#	send back Form for comment.(js)
	#return jsonify(texts[11])

	story = {'title':'My Story', 'author':'Juan David', 'year': 2019, 'text': 'This is my first Story.'}
	comments = [{"text":"1st. comment. hello"}, {"text":"2nd. comment. world"}]
	return render_template("story_page.html", story=story, comments=comments)


@app.route("/channelslist")
def channelslist():

	#Send a list of links to channels.

	return render_template("channels_list.html")

@app.route("/channellist")
def channellist():

	#Send a list of links to channels.
	#return render_template("channels_list.html")
	return jsonify(texts[15])


	


if __name__ == "__main__":
	app.run()

