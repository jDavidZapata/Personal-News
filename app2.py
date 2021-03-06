from flask import Flask, flash, redirect, render_template, request, session, abort, redirect, url_for, g, jsonify
import os, requests, json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
#from flask_socketio import SocketIO
''' add support for webSockets.
    add flash=k-login support. 
    add variable to support for local storage on the client side. '''


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

app.secret_key = b'_3#y2L"F4Q8z\n\xec]/'


# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET", "POST"])
def index():

    error = None

    """Check to see if User is in session."""

    user_id = session.get('user_id')

    if (not 'user_id' in session):
        g.user = None

        return render_template("index.html", error=error)

    else:
        g.user = db.execute(
            'SELECT * FROM users WHERE id IN (:id)', {"id": user_id, }
        ).fetchone()

        return render_template("index.html", error=error)


@app.route('/register', methods=('GET', 'POST'))
def register():
    """Register a new user.
        Check if the user is in session.
        Validates that the name and email are not already taken. 
        Redirect to index page.
        #Hashes the password for security.
    """
    error = None

    success = None

    user_id = session.get('user_id')

    if ('user_id' in session):

        g.user = db.execute(
            'SELECT * FROM users WHERE id IN (:id)', {"id": user_id, }
        ).fetchone()

        # change to redirect to current page
        return render_template("index.html")

    if request.method == 'POST':

        name = request.form['name']
        password = request.form['password']
        email = request.form['email']

        error = None

        if not name:
            error = 'Name is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email required.'

        user = db.execute("SELECT * FROM users WHERE email IN (:email)",
                          {"email": email}).fetchone()

        if user is not None:
            error = 'User with email {0} is already registered.'.format(email)

        if error is None:
            """If the name is available, store it in the database and go to the login page"""

            db.execute("INSERT INTO users (name, password, email) VALUES (:name, :password, :email)",
                       {"name": name, "password": password, "email": email})
            db.commit()

            user = db.execute("SELECT * FROM users WHERE email IN (:email)", {
                              "email": email}).fetchone()

            """Store the user id in a new session and return to the index"""

            session.clear()
            session['user_id'] = user['id']
            g.user = user

            '''
            g.user = db.execute(
                'SELECT * FROM users WHERE id IN (:id)', {"id": user_id, }
            ).fetchone()
            '''

            success = 'Thank You For Signing Up.'

            # Change to redirect to curent page
            return redirect(url_for('index'))

    return render_template('auth/register.html', error=error, success=success)


@app.route('/login', methods=('GET', 'POST'))
def login():
    """Log in a registered user by adding the user id to the session."""

    error = None

    success = None

    user_id = session.get('user_id')

    if ('user_id' in session):
        g.user = db.execute(
            'SELECT * FROM users WHERE id IN (:id)', {"id": user_id, }
        ).fetchone()

        # change to redirect to current page
        return render_template("index.html", error=error)

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        error = None

        user = db.execute("SELECT * FROM users WHERE email IN (:email) AND password IN (:password)",
                          {"email": email, "password": password}).fetchone()

        if user is None:
            error = 'Incorrect Email or Password.'

        if error is None:

            """Store the user id in a new session and return to the index."""
            session.clear()
            session['user_id'] = user['id']
            g.user = db.execute(
                'SELECT * FROM users WHERE id IN (:id)', {"id": user_id, }
            ).fetchone()
            db.close()

            success = 'Your Now Signed In.'

            return redirect(url_for('index'))

    return render_template('auth/login.html', error=error, success=success)


@app.route('/logout')
def logout():

    success = None

    """Clear the current session, including the stored user id."""
    session.clear()
    g.user = None

    success = 'Your Now Loged Out.'

    return redirect(url_for('index', success=success))


@app.route('/channel_list', methods=('GET', 'POST'))
def channel_list():



@app.route('/channel', methods=('GET', 'POST'))
def channel_page():


@app.route('/channel_create', methods=('GET', 'POST'))
def channel_create():


@app.route('/pstory', methods=('GET', 'POST'))
def pstory_newslink_page():


@app.route('/categorie', methods=('GET', 'POST'))
def categori():