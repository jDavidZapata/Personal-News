from flask import Flask, render_template, jsonify
import requests, json
import os
from models import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
db.init_app(app)


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
				#return new_dic


messages = []
key1 = 'messages'

get_whatever_list(channels, key1, messages)


'''
messages = []

def get_messages(channels):
	for c in channels:
		if 'messages' in c:
			for i in c['messages']:
				messages.append(i)

get_messages(channels)
'''
		
#messages = [channels[i]['messages'] if 'messages' in channels[i] else "No Messages." for i in range(len(channels))]

print(f'Unfilter Messages 0:{messages}')


storys = []
key2 = 'storys'
get_whatever_list(channels, key2, storys)

'''
for c in channels:
	if 'storys' in c:
		for i in c['storys']:
			storys.append(i)
'''


print(f"Storys 0: {storys}")


comments = []
key3 = 'comments'
get_whatever_list(storys, key3, comments)

'''
for s in storys:
	if 'comments' in s:
		for i in s['comments']:
			comments.append(i)
'''


print(f"comments 0: {comments}")



storys_0 = [{"title": "A story", "text": "this is my first story."},{"title": "Another story", "text": "this is my second story."} ]

messages_0 = [{"text":"hello, 1st message"}, {"text":"world, 2nd message"}, {"text":"And this is the 3rd message."}]

story_0 = {'title':'My Story', 'author':'Juan David', 'year': 2019, 'text': 'This is my first Story.'}

comments_0 = [{"text":"1st. comment. hello"}, {"text":"2nd. comment. world"}]

texts = ["Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam tortor mauris, maximus semper volutpat vitae, varius placerat dui. Nunc consequat dictum est, at vestibulum est hendrerit at. Mauris suscipit neque ultrices nisl interdum accumsan. Sed euismod, ligula eget tristique semper, lectus est pellentesque dui, sit amet rhoncus leo mi nec orci. Curabitur hendrerit, est in ultricies interdum, lacus lacus aliquam mauris, vel vestibulum magna nisl id arcu. Cras luctus tellus ac convallis venenatis. Cras consequat tempor tincidunt. Proin ultricies purus mauris, non tempor turpis mollis id. Nam iaculis risus mauris, quis ornare neque semper vel.",
		"Praesent euismod auctor quam, id congue tellus malesuada vitae. Ut sed lacinia quam. Sed vitae mattis metus, vel gravida ante. Praesent tincidunt nulla non sapien tincidunt, vitae semper diam faucibus. Nulla venenatis tincidunt efficitur. Integer justo nunc, egestas eget dignissim dignissim, fermentum ac sapien. Suspendisse non libero facilisis, dictum nunc ut, tincidunt diam.",
		"Morbi imperdiet nunc ac quam hendrerit faucibus. Morbi viverra justo est, ut bibendum lacus vehicula at. Fusce eget risus arcu. Quisque dictum porttitor nisl, eget condimentum leo mollis sed. Proin justo nisl, lacinia id erat in, suscipit ultrices nisi. Suspendisse placerat nulla at volutpat interdum. In porttitor condimentum est nec ultricies. Donec nec mollis neque, id dapibus sem.",
		"Home", "Caterory", "Create Category", "Create Channel", "Log Out", "Log In", "Register", "Channel Page", "Story Page", "List of News Links", "list of categories", "category:[happy,romantic,sad]", "'channel list':['Channel1', 'channel2', 'channel3', 'channel4', 'channel5']"]


@app.route("/")
def index():

	res = requests.get("https://api.nytimes.com/svc/topstories/v2/home.json", params={"api-key": os.getenv("API_KEY")})
		
	if res.status_code != 200:
		raise Exception("ERROR: API request unsuccessful.")
				
	data = res.json()

	results = data['results']

	
	'''
	result = []
	r = {}
	i = 0

	for i in range(len(results)):
		
		r['section'] = (results[i]['section'])
		r['title'] = (results[i]['title'])
		r['abstract'] = (results[i]['abstract'])
		r['url'] = (results[i]['url'])
		
		result.append(r)

	'''
	#r = [{'title': results[i]['title'], 'section' : results[i]['section'], 'abstract' : results[i]['abstract'], 'url' : results[i]['url'], 'multimedia' : results[i]['multimedia'][2]} for i in range(len(results))]

	# result = [x for x in results[range(len(results))]]

	#results = data['results'][0]['title']


	links = [{'title': results[i]['title'], 'section' : results[i]['section'], 'abstract' : results[i]['abstract'], 
			'url' : results[i]['url'], 'multimedia' : (results[i]['multimedia'][2] if results[i]['multimedia'] 
			else results[i]['multimedia']) } for i in range(len(results))]
	

	#print(storys)

	return render_template("index.html", links=links)



@app.route("/category/<string:category_title>", methods=['GET', 'POST'])
def home(category_title):

	# Make Api call to NYT for Top Story's News links.
	# Send list News links. 
	#  return jsonify(f"{texts[3]} =======>>>>    {texts[0]}")


	print(f"category title: {category_title}")

	res = requests.get(f"https://api.nytimes.com/svc/topstories/v2/{category_title}.json", params={"api-key": os.getenv("API_KEY")})
		
	if res.status_code != 200:
		raise Exception("ERROR: API request unsuccessful.")
				
	data = res.json()

	results = data['results']

	links = [{'title': results[i]['title'], 'section' : results[i]['section'], 'abstract' : results[i]['abstract'], 'url' : results[i]['url'], 'multimedia' : (results[i]['multimedia'][2] if results[i]['multimedia'] else results[i]['multimedia']) } for i in range(len(results))]

	#print(storys)

	return render_template("index.html", links=links)
	


@app.route("/category")
def category():

	#Send a list of links to categories.
	# js will take responce and and display div with links to route that will search that category.
	# html should 
	#return jsonify(texts[4], texts[13], texts[14])

	categories =  "arts,automobiles,books,business,fashion,food,health,home,insider,magazine,movies,national,nyregion,obituaries,opinion,politics,realestate,science,sports,sundayreview,technology,theater,tmagazine,travel,upshot,world"

	categorys = categories.split(',')

	print(categorys)

	return render_template("category.html", categorys=categorys)


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




@app.route("/channelPage/<string:channel_title>", methods=['GET', 'POST'])
def channelPage(channel_title):

	# route takes GET request with a name string... 
	# looks for that string channel name and returns it.
	# else returns channels page with channel not found error.

	#Send back list of news links on channel.
	#Send back first 100 messages.
	#Send back Form for messages.(JS)
	#return jsonify(texts[10])

	#ch = [(channels[i] if channel_title in channels[i]['title'] else None) for i in range(len(channels))]
	
	
	'''
	channel = []
	print(f"Unfilter Channel:{ch}") 
	print()

	for s in ch:				
		if s != None:
			channel.append(s)
	
	'''

	'''

	def get_whatever_dic (objs_list, key, value, new_dic):
		for c in objs_list:
			if c[key] == value:
				new_dic = c

	'''
	
	'''
	channel = {}
	key4 = 'title'
	value1 = channel_title
	get_whatever_dic(channels, key4, value1, channel)
	


	'''
	channel = {}
	for c in channels:
		if c['title'] == channel_title:
			channel = c
	

	print(f'Unfilter Channel:{channel}')

	ch = channel



	'''
	messages = []


	if 'messages' in channel[0]:
			messages.append(channel[0]['messages'])

	'''
	
	#messages = channel[0]['messages'] if 'messages' in channel[0] else "No Messages."

	messages = ch['messages'] if 'messages' in ch else "No Messages."

	#storys = channel[0]['storys'] if 'storys' in channel[0] else "No Story's."
	storys = channel['storys'] if 'storys' in channel else "No Story's."
	
	
	if channel:
		info = {'title': channel['title'], 'year': channel['year'], 'author': channel['author'], 'text': channel['text']}
	else:
		info = {}	


	print(f"Messages: {messages}")

	print(f"Filter Channel: {ch}")

	print(f"Story's: {storys}")

	print(f"Channel info: {info}")

	if channel == None:

		error = "No Channel"

		return render_template("channels_list.html", error=error)

	'''
	channel = {"title":"My Channel", "author":"Juan David", "year": 2019, "text": "This is My Channel."}
	storys = [{"title": "A story", "text": "this is my first story."},{"title": "Another story", "text": "this is my second story."} ]
	messages = [{"text":"hello, 1st message"}, {"text":"world, 2nd message"}, {"text":"And this is the 3rd message."}]
	'''

	return render_template("channel_page.html", channel=channel, messages=messages, storys=storys, info=info)


@app.route("/storyPage/<string:story_title>", methods=['GET', 'POST'])
def storyPage(story_title):	

	# Display Story.
	# take in <storyID>
	#	Send back Story title, text.
	#	Send back first 10 out of 100 comments.
	#	send back Form for comment.(js)
	# for link just save the url
	#return jsonify(texts[11])
	
	'''
	story = []

	for s in storys:
		if s['id'] == story_id:
			story.append(s)
	

	print(f'Unfilter Story:{story}')


	'''
	print(f"title ==== {story_title}")
	print(f"@@@======>>Storys{storys}")

	'''
	story = {}
	key5 = 'title'
	value2 = story_title
	get_whatever_dic(storys, key5, value2, story)
	

	'''
	story = {}
	for s in storys:
		if s['title'] == story_title:
			story = s
	

	print(f'Unfilter storryy:{story}')

	
	comments = story['comments'] if 'comments' in story else "No Comments."

	links = story['links'] if 'links' in story else "No Links."
	
	print(f"Filter comments: {comments}")

	#story = {'title':'My Story', 'author':'Juan David', 'year': 2019, 'text': 'This is my first Story.'}
	#comments = [{"text":"1st. comment. hello"}, {"text":"2nd. comment. world"}, {"text":"3. comment. "}, {"text":"4. comment. "}, {"text":"5. comment. hello"}, {"text":"6. comment. world"}]
	#links = [{'link': 1, 'url': 'url1', 'img': 'img1'}, {'link': 2, 'url': 'url2', 'img': 'img2'}, {'link': 3, 'url': 'url3', 'img': 'img3'}]

	return render_template("story_page.html", story=story, comments=comments, links=links)


@app.route("/channelslist")
def channelslist():

	#Send a list of links to channels.
	# link
	'''
	channel1 = {"title":"My Channel", "author":"Juan David", "year": 2019, "text": "This is My Channel."}

	channel2 = {"title":"Daves Channel", "author":"Dave", "year": 2019, "text": "This is daves Channel."}

	channel3 = {"title":"juans Channel", "author":"Juan", "year": 2019, "text": "This is Juans Channel."}

	channels = [channel1, channel2, channel3]
	'''

	

	return render_template("channels_list.html", channels=channels)

@app.route("/storyslist")
def storyslist():

	#Send a list of links to storys.

	


	return render_template("storys_list.html", storys=storys)
	


	


if __name__ == "__main__":
	app.run()

