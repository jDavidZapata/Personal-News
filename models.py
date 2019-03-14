import os
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    channel = db.relationship("Channel", backref="channel_owner", lazy=True)
    storys = db.relationship("Story", backref="story_owner", lazy=True)
    messages = db.relationship("Message", backref="message_owner", lazy=True)

    def __init__(self, name, username, nohash_password, email):
        self.name = name
        self.username = username
        self.password = generate_password_hash(nohash_password)
        self.email = email


    def __repr__(self):
        return '<User %r>' % self.username

    
    def set_password(self, nohash_password):
        self.password = generate_password_hash(nohash_password)

    def check_password(self, nohash_password):
        return check_password_hash(self.password, nohash_password)


    def add_channel(self, user_id, title, text, user):
        c = Channel(user_id=self.id, title=title, text=text, user=self)
        db.session.add(c)
        db.session.commit()

    def add_story(self, user_id, channel_id, title, story_text, user, channel):
        s = Story(user_id=self.id, channel_id=channel_id, title=title, story_text=story_text, user=self, channel=channel)
        db.session.add(s)
        db.session.commit()

    def add_message(self, user_id, channel_id, message_text, user, channel):
        m = Message(user_id=self.id, channel_id=channel_id, message_text=message_text, user=self, channel=channel)
        db.session.add(m)
        db.session.commit()

    def add_comment(self, user_id, story_id, comment_text, user, story):
        c = Comment(user_id=self.id, story_id=story_id, comment_text=comment_text, user=self, story=story)
        db.session.add(c)
        db.session.commit()

    def add_link(self, user_id, story_id, text, url, user, story):
        l = Link(user_id=self.id, story_id=story_id, text=text, url=url, user=self, story=story)
        db.session.add(l)
        db.session.commit()


class Channel(db.Model):
    __tablename__ = "channels"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    title = db.Column(db.String, nullable=False, unique=True)
    text = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    storys = db.relationship("Story", backref="channels_storys", lazy=True)
    messages = db.relationship("Message", backref="channels_messages", lazy=True)
    user = db.relationship("User", backref="channel_owner", uselist=False, lazy=True)

    def __init__(self, user_id, title, text, user, storys=[], messages=[]):
        self.user_id = user_id
        self.title = title
        self.text = text
        self.user = user
        
    def __repr__(self):
        return '<Channel title: %r>' % self.title


    def add_story_(self, user_id, channel_id, title, story_text, user, channel):
        s = Story(user_id=user_id, channel_id=self.id, title=title, story_text=story_text, user=user, channel=self)
        db.session.add(s)
        db.session.commit()

    def add_message_(self, user_id, channel_id, message_text, user, channel):
        m = Message(user_id=user_id, channel_id=self.id, message_text=message_text, user=user, channel=self)
        db.session.add(m)
        db.session.commit()


class Story(db.Model):
    __tablename__ = "storys"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey("channels.id"), nullable=False)
    title = db.Column(db.String, nullable=False)
    story_text = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user = db.relationship("User", backref="story_owner", uselist=False, lazy=True)
    channel = db.relationship("Channel", backref="story_channel", uselist=False, lazy=True)
    comments = db.relationship("Comment", backref="storys_comments", lazy=True)
    links = db.relationship("Link", backref="storys_links", lazy=True)

    def __init__(self, user_id, channel_id, title, story_text, user, channel):
        self.user_id = user_id
        self.channel_id =channel_id
        self.title = title
        self.story_text = story_text
        self.user = user
        self.channel = channel


    def add_comment_(self, user_id, story_id, comment_text, user, story):
        c = Comment(user_id=user_id, story_id=self.id, comment_text=comment_text, user=user, story=self)
        db.session.add(c)
        db.session.commit()

    def add_link_(self, user_id, story_id, text, url, user, story):
        l = Link(user_id=user_id, story_id=self.id, text=text, url=url, user=user, story=self)
        db.session.add(l)
        db.session.commit()


    def __repr__(self):
        return '<Story Title: %r>' % self.title


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey("channels.id"), nullable=False)
    message_text = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user = db.relationship("User", backref="message_owner", uselist=False, lazy=True)
    channel = db.relationship("Channel", backref="channel_message", uselist=False, lazy=True)

    def __init__(self, user_id, channel_id, message_text, user, channel):
        self.user_id = user_id
        self.channel_id =channel_id
        self.message_text = message_text
        self.user = user
        self.channel = channel


    def __repr__(self):
        return '<Message: %r>' % self.message_text

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    story_id = db.Column(db.Integer, db.ForeignKey("storys.id"), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user = db.relationship("User", backref="comment_owner", uselist=False, lazy=True)
    story = db.relationship("Story", backref="story_comment", uselist=False, lazy=True)

    def __init__(self, user_id, story_id, comment_text, user, story):
        self.user_id = user_id
        self.story_id =story_id
        self.comment_text = comment_text
        self.user = user
        self.story = story


    def __repr__(self):
        return '<Comment: %r>' % self.comment_text


class Link(db.Model):
    __tablename__ = "links"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    story_id = db.Column(db.Integer, db.ForeignKey("storys.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    url = db.Column(db.String, nullable=False)
    user = db.relationship("User", backref="link_owner", uselist=False, lazy=True)
    story = db.relationship("Story", backref="link_story", uselist=False, lazy=True)



    def __init__(self, user_id, story_id, text, url, user, story):
        self.user_id = user_id
        self.story_id =story_id
        self.text = text
        self.url = url
        self.user = user
        self.story = story

    def __repr__(self):
        return '<Link: %r>' % self.url
