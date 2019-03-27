from flask import Flask, render_template, jsonify, session, url_for, request, redirect, g, flash
import requests, json
from models import *
from forms import RegistrationForm, LoginForm, CreateChannelForm, CreateStoryForm, MessageForm, CommentForm
from config import *
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_migrate import Migrate
from werkzeug.urls import url_parse
from flask_socketio import SocketIO, emit, join_room, leave_room
import os


app = Flask(__name__)

#app.config.from_object(DevelopmentConfig)
app.config.from_object(os.environ['APP_SETTINGS'])

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
#app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
migrate = Migrate(app, db)

login_ = LoginManager(app)
login_.login_view = 'login'

socketio = SocketIO(app)

@login_.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500



channel = None


channel1 = {"title":"Channel-test", "author":"my self", "year": 2020, "text": "This is A Channel.", 'messages' : [{"text":"hello, 1st message"}, {"text":"world, 2nd message"}, {"text":"And this is the 3rd message."}], 'storys': [{"title": "1 story", 'author':'Juan David', 'year': 2019, "text": "first story.", 'comments' : [{'text':"1st. comment. hello"}, {'text':"2nd. comment. world"}]},{"title": "2 story", 'author':'Juan David', 'year': 2019, "text": "2nd story."},{'title':'My Story', 'author':'Juan David', 'year': 2019, 'text': 'This is my first Story.', 'links': [{'link': 1, 'url': 'url1', 'img': 'img1'}, {'link': 2, 'url': 'url2', 'img': 'img2'}, {'link': 3, 'url': 'url3', 'img': 'img3'}], 'comments': [{"text":"1st. comment. hello"}, {"text":"2nd. comment. world"}, {"text":"3. comment. "}, {"text":"4. comment. "}, {"text":"5. comment. hello"}, {"text":"6. comment. world"}]}]}

channel2 = {"title":"My Channel", "author":"Juan David", "year": 2019, "text": "This is My Channel.", 'messages' : [{"text":" 1st message"}, {"text":"2nd message"}, {"text":"3rd message."}], 'storys': [{"title": "A 1 story", 'author':'David', 'year': 2018, "text": "this is my first story."},{"title": "Another story", 'author':'Juavid', 'year': 2029, "text": "this is my 2nd story."}]}

channel3 = {"title":"Daves Channel", "author":"Dave", "year": 2019, "text": "This is daves Channel.", 'storys' : [{"title": "A story", 'author':'Jd', 'year': 2029, "text": "This is my 1st story."},{"title": "MY SECOND story", 'author':'JDz', 'year': 2017, "text": "This is my second story."} ]}

channel4 = {"title":"juans Channel", "author":"Juan", "year": 2019, "text": "This is Juans Channel.", 'storys' : [{"title": "story", 'author':'Juan Dz', 'year': 2017, "text": "A story."}]}

channel5 = {"title":"Dman's Channel", "author":"DMAN", "year": 2018, "text": "This DMAN Channel."}


channels = [channel5, channel1, channel2, channel3, channel4]


def get_whatever_list(list_of_obj, key, new_list):
	for c in list_of_obj:
		if key in c:
			for i in c[key]:
				new_list.append(i)



def get_whatever_dic (objs_list, key, value, new_dic):
		for c in objs_list:
			if value in c[key]:  
				new_dic = c
				print(f"new_dic = {new_dic}")
				


messages = []
key1 = 'messages'

get_whatever_list(channels, key1, messages)


storys = []
key2 = 'storys'
get_whatever_list(channels, key2, storys)


comments = []
key3 = 'comments'
get_whatever_list(storys, key3, comments)


@app.route("/")
def index():

	res = requests.get("https://api.nytimes.com/svc/topstories/v2/home.json", params={"api-key": os.getenv("API_KEY")})
		
	if res.status_code != 200:
		raise Exception("ERROR: API request unsuccessful.")
				
	data = res.json()

	results = data['results']
	
	links = [{'title': results[i]['title'], 'section' : results[i]['section'], 'abstract' : results[i]['abstract'], 
			'url' : results[i]['url'], 'multimedia' : (results[i]['multimedia'][2] if results[i]['multimedia'] 
			else results[i]['multimedia']) } for i in range(len(results))]    
	
	return render_template("index.html", links=links)



@app.route('/register', methods=['GET', 'POST'])
def register():
	""" Register a new user. """
	""" Check if is user is authenticated, then user already register. """
	if current_user.is_authenticated:
		return redirect(url_for('index'))
		
	form = RegistrationForm()
	""" Get values from form. """
	
	if form.validate_on_submit():
		""" Make sure email is not already register. """
		"""If the email is available, store it in the database and go to the login page. """

		user = User(name=form.name.data, username=form.username.data, nohash_password=form.password.data, email=form.email.data)
		#user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')		

		return redirect(url_for('login'))

	return render_template('auth/register.html', title='Register', form=form)




@app.route('/login', methods=['GET', 'POST'])
def login():
	""" Log in a registered user. """
	"""If the users is authenticated, then user already loged in."""

	if current_user.is_authenticated:
		return redirect(url_for('index'))
		
	form = LoginForm()
	""" Get values from form. """

	if form.validate_on_submit():
		""" Get User from DataBase using Email. """

		user = User.query.filter_by(email=form.email.data).first()

		flash('Login requested for user {}, remember_me={}'.format(form.email.data, form.remember_me.data))
		
		if user is None or not user.check_password(form.password.data):
			flash('Invalid email or password')
			return redirect(url_for('login'))

		""" If there is A User, then log them in. """
		login_user(user, remember=form.remember_me.data)

		""" Redirect to the next page if there was one, else go to main page. """
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')

		return redirect(next_page)

	return render_template('auth/login.html', title='Sign In', form=form)


@app.route("/logout")
def logout():

	""" Long out user. """
	
	logout_user()
	flash('Loging Out the User... Comeback soon...')
	
	return redirect(url_for('index'))

    
@app.route("/category")
def category():
	""" List of Categories. """

	categories =  "arts,automobiles,books,business,fashion,food,health,home,insider,magazine,movies,national,nyregion,obituaries,opinion,politics,realestate,science,sports,sundayreview,technology,theater,tmagazine,travel,upshot,world"

	categorys = categories.split(',')
	
	return render_template("category.html", categorys=categorys)


@app.route("/channelslist")
def channelslist():
	""" List of channels. """
	""" Get all Channels From DataBase. """

	channels = Channel.query.all()
	
	return render_template("channels_list.html", channels=channels)


@app.route("/storyslist")
def storyslist():
	""" List of Storys. """
	""" Get Storys From DataBase. """

	storys = Story.query.all()

	return render_template("storys_list.html", storys=storys)
	


@app.route("/category/<string:category_title>", methods=['GET', 'POST'])
@login_required
def home(category_title):
	""" List of news links. """
	""" Make API call to NYT for Top Story's Section News links. """	
	
	res = requests.get(f"https://api.nytimes.com/svc/topstories/v2/{category_title}.json", params={"api-key": os.getenv("API_KEY")})
		
	if res.status_code != 200:
		raise Exception("ERROR: API request unsuccessful.")
				
	data = res.json()

	results = data['results']
	
	""" Send Lik Data. """
	links = [{'title': results[i]['title'], 'section' : results[i]['section'], 'abstract' : results[i]['abstract'], 'url' : results[i]['url'], 
			'multimedia' : (results[i]['multimedia'][2] if results[i]['multimedia'] else results[i]['multimedia']) } for i in range(len(results))]

	return render_template("index.html", links=links)
	



@app.route("/channelPage/<string:channel_title>", methods=['GET', 'POST'])
def channelPage(channel_title):
	""" Channel Page. """
	""" Route takes GET request with title string.
		Looks for that string channel name and returns it.
		Else returns channels page with channel not found error. """
	
	""" Get Channel From DataBase if it exists. """	
	channel = Channel.query.filter_by(title=channel_title).first_or_404()
	#channel = Channel.query.filter_by(title=channel_title).first()	
	""" If there is no Channel, redirect to Channels list. """
	if channel == None:

		error = "No Channel"

		return render_template("channels_list.html", error=error)

	""" Channel Info. """
	
	""" list of Messages from Channel. Send first 20. """
	messages = channel.messages
	
	if not messages:
		messages = "No Messages."

	""" List of Storys from Channel. Send first 20. """
	storys = channel.storys 
	
	if not storys:
		storys = "No Storys."
	
	form = MessageForm()
	""" Get values from form. """
	
	if form.validate_on_submit():
		""" Make sure . """
		
		message = Message(user_id=current_user.id, channel_id=channel.id, message_text=form.message_text.data, user=current_user, channel=channel)
		db.session.add(message)
		db.session.commit()		
		
		return render_template("channel_page.html", channel=channel, messages=messages, storys=storys, form=form)

	return render_template("channel_page.html", channel=channel, messages=messages, storys=storys, form=form)


@app.route("/storyPage/<int:story_id>", methods=['GET', 'POST'])
def storyPage(story_id):
	""" Story Page. """	
	""" Route takes GET request with title string.
		Looks for that string story name and returns it.
		Else returns storys page with story not found error.
		Fix if story doesnt have a unique title then look it up by id """

	""" Get Story From DataBase if it exists. """
	story = Story.query.filter_by(id=story_id).first_or_404()

	""" If there is no Story, redirect to Storys list. """
	if story == None:
		error = "No Story"

		return render_template("storys_list.html", error=error)

	""" list of Comments from Story. Send first 20. """
	comments = story.comments
	
	if not comments:
		comments = "No Comments."

	""" List of Links from Story. Send first 20. """
	links = story.links
	
	if not links:
		links = "No Links."

	form = CommentForm()
	""" Get values from form. """
	
	if form.validate_on_submit():
		""" Make sure . """
		
		comment = Comment(user_id=current_user.id, story_id=story.id, comment_text=form.comment_text.data, user=current_user, story=story)
		db.session.add(comment)
		db.session.commit()				
		
		return render_template("story_page.html", story=story, comments=comments, links=links, form=form)
	
	return render_template("story_page.html", story=story, comments=comments, links=links, form=form)




@app.route("/createChannel", methods=['GET', 'POST'])
@login_required
def createChannel():
	""" Create A Channel. """
			
	form = CreateChannelForm()
	""" Get values from form. """
	
	if form.validate_on_submit():
		""" Check User doesnt already have a Channel. """
		""" If User has Channel redirect to channel. """		
		
		ch = Channel.query.filter_by(user=current_user).first()
		if ch is not None:
			flash('You Already Have A Channel.')
			return redirect(url_for('createChannel'))
		
		""" Add Channel. """
		channel = Channel(user_id=current_user.id, title=form.title.data, text=form.text.data, user=current_user)
		db.session.add(channel)

		""" Add Message if any. """
		if form.message.data:
			message = Message(user_id=current_user.id, channel_id=channel.id, message_text=form.message.data, user=current_user, channel=channel)
			
			db.session.add(message)		
		
		""" Commit changes to DataBase. """
		db.session.commit()
		flash('Congratulations, you Added Your Channel!')		
		
		return redirect(url_for('channelPage', channel_title=form.title.data))

	return render_template("channel_create.html", form=form)


@app.route("/createStory", methods=['GET', 'POST'])
@login_required
def createStory():
	""" Create A Story. """

	form = CreateStoryForm()
	""" Get values from form. """
	
	if form.validate_on_submit():
		""" Check that User doesn't have a Story with same title. """

		channel = Channel.query.filter_by(user=current_user).first()
		if channel is None:
			flash("You Don't Have A Channel.")
			return redirect(url_for('createChannel'))

		st = Story.query.filter_by(user_id=current_user.id, title=form.title.data).first()
		if st is not None:
			flash('You Already Have A Story with this Title.')

			return redirect(url_for('createStory'))
				
		""" Add Story. """
		story = Story(user_id=current_user.id, channel_id=channel.id, title=form.title.data, story_text=form.story_text.data, user=current_user, channel=channel)
		db.session.add(story)

		""" Add Comments if any. """
		if form.comment.data:
			comment = Comment(user_id=current_user.id, story_id=story.id, comment_text=form.comment.data, user=current_user, story=story)
		
			db.session.add(comment)					
		
		""" Commit changes to DataBase. """
		db.session.commit()
		flash('Congratulations, you Added A Story!')	
		
		return redirect(url_for('storyPage', story_id=story.id))
		
	return render_template("story_create.html", form=form)



@socketio.on("join")
def on_join(data):
	""" Place User in room. """ 
	""" Get room from Data. """
	print(f" < === DATA  joining === > {data}")
	user = current_user
	room = data['room']

	""" If TITLE get Channel, If ID get Story. """ 
	# channel = Channel.query.filter_by(title=channel_title).first()
	# story = Story.query.filter_by(id=story_id).first()
	
	""" Join Room. """
	join_room(room)
	print(f" < == User {user} === join  {room} Room == > ")
	


@socketio.on("leave")
def on_leave(data):
	""" Take User Out of room. """ 
	""" Get room from Data. """
	print(f" < === DATA leaving === > {data}")
	user = current_user
	room = data['room']

	""" If TITLE get Channel, If ID get Story. """
	#channel = Channel.query.filter_by(title=channel_title).first()
	# story = Story.query.filter_by(id=story_id).first()
	
	""" Leave Room. """
	leave_room(room)
	print(f" < == User {user} === Leave  {room} Room == > ")
	


@socketio.on("leave1")
def on_leave1(data):
	""" Take User Out of room. """ 
	""" Get room from Data. """
	print(f" < === Finally Leaving Data === > {data}")
	user = current_user
	room = data['room']

	""" If TITLE get Channel, If ID get Story. """
	#channel = Channel.query.filter_by(title=channel_title).first()
	# story = Story.query.filter_by(id=story_id).first()
	
	""" Leave Room. """
	leave_room(room)
	print(f" < == User {user} === Is Finally Leaving  {room} Room == > ")


	
@socketio.on("submit message")
def message(data):
	""" New Messages. """
	""" Get message and Channel title from Data. """
	print(f"New Message DATA === > {data}")
	text = data["message"]
	channel_title = data['channel_t']
	room = channel_title
	user = current_user

	""" Make sure Channel exists. (write if loop)"""
	channel = Channel.query.filter_by(title=channel_title).first()
	
	""" Add Message to DataBase and commit changes. """
	message = Message(user_id=user.id, channel_id=channel.id, message_text=text, user=user, channel=channel)
	db.session.add(message)
	db.session.commit()
	
	""" Send Message to everyone in Room. """
	print(f" < ==  Message: {text} ===  Channel: {channel} == > ")
	print(f"current_user === > {user}")
	data = {'text': text, 'user': user.name}
	emit("new message", data, broadcast=True, room=room)


@socketio.on("submit comment")
def comment(data):
	""" New Comments. """
	""" Get comment and Story ID from Data. """
	print(f"New Comment DATA === > {data}")
	text = data["comment"]
	story_id = data['story_id']
	room = story_id
	user = current_user

	""" Make sure Story exists. (write if loop)"""
	story = Story.query.filter_by(id=story_id).first()

	""" Add Comment to DataBase and commit changes. """
	comment = Comment(user_id=user.id, story_id=story_id, comment_text=text, user=user, story=story)
	db.session.add(comment)
	db.session.commit()
	
	""" Send Comment to everyone in Room. """
	data = {'text': text, 'user': user.name}
	emit("new comment", data, broadcast=True, room=room)


if __name__ == "__main__":
	app.run()

