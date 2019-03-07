import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    channel = db.relationship("Channel", backref="user", lazy=True)
    storys = db.relationship("Story", backref="user", lazy=True)
    messages = db.relationship("Message", backref="user", lazy=True)


    def __repr__(self):
        return '<User %r>' % self.name

    def add_channel(self, user_id, title, text, time):
        c = Channel(user_id=self.id, title=title, text=text, time=time)
        db.session.add(c)
        db.session.commit()

    def add_story(self, user_id, channel_id, title, story_text, time):
        s = Story(user_id=self.id, channel_id=channel_id, title=title, story_text=story_text, time=time)
        db.session.add(s)
        db.session.commit()

    def add_message(self, user_id, channel_id, message_text, time):
        m = Message(user_id=self.id, channel_id=channel_id, message_text=message_text, time=time)
        db.session.add(m)
        db.session.commit()

    def add_comment(self, user_id, story_id, comment_text, time):
        c = Comment(user_id=self.id, story_id=story_id, comment_text=comment_text, time=time)
        db.session.add(c)
        db.session.commit()

    def add_link(self, user_id, story_id, url, text):
        l = Link(user_id=self.id, story_id=story_id, url=url, text=text)
        db.session.add(l)
        db.session.commit()


class Channel(db.Model):
    __tablename__ = "channels"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    title = db.Column(db.String, nullable=False, unique=True)
    text = db.Column(db.Text, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    storys = db.relationship("Story", backref="channel", lazy=True)
    messages = db.relationship("Message", backref="channel", lazy=True)
    user = db.relationship("User", backref=backref("channel", uselist=False), lazy=True)

    def __repr__(self):
        return '<Channel title: %r>' % self.title


    def add_story_(self, user_id, channel_id, title, story_text, time):
        s = Story(user_id=user_id, channel_id=self.id, title=title, story_text=story_text, time=time)
        db.session.add(s)
        db.session.commit()

    def add_message_(self, user_id, channel_id, message_text, time):
        m = Message(user_id=user_id, channel_id=self.id, message_text=message_text, time=time)
        db.session.add(m)
        db.session.commit()


class Story(db.Model):
    __tablename__ = "storys"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey("channels.id"), nullable=False)
    title = db.Column(db.String, nullable=False, unique=True)
    story_text = db.Column(db.Text, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    user= db.relationship("User", backref=backref("story", uselist=False), lazy=True)
    comments = db.relationship("Comment", backref="story", lazy=True)
    links = db.relationship("Link", backref="story", lazy=True)

    def add_comment_(self, user_id, story_id, comment_text, time):
        c = Comment(user_id=user_id, story_id=self.id, comment_text=comment_text, time=time)
        db.session.add(c)
        db.session.commit()

    def add_link_(self, user_id, story_id, url, text):
        l = Link(user_id=user_id, story_id=self.id, url=url, text=text)
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
    time = db.Column(db.Integer, nullable=False)
    user = db.relationship("User", backref=backref("message", uselist=False), lazy=True)

    def __repr__(self):
        return '<Message: %r>' % self.message_text

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    story_id = db.Column(db.Integer, db.ForeignKey("storys.id"), nullable=False)
    commet_text = db.Column(db.Text, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    user = db.relationship("User", backref=backref("comment", uselist=False), lazy=True)

    def __repr__(self):
        return '<Comment: %r>' % self.comment_text


class Link(db.Model):
    __tablename__ = "links"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    story_id = db.Column(db.Integer, db.ForeignKey("storys.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    url = db.Column(db.String, nullable=False)
    user = db.relationship("User", backref=backref("link", uselist=False), lazy=True)

    def __repr__(self):
        return '<Link: %r>' % self.url
