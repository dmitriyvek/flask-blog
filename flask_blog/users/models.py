import datetime

from werkzeug.security import generate_password_hash

from flask_blog import db
from flask_blog.blog.models import Post


class User(db.Model):
    '''The common model used for user`s authorization'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    registered_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    admin = db.Column(db.Boolean, nullable=False, default=False)

    # post_list = db.relationship('Post', backref=db.backref(
    #     'author'), cascade="all, delete")

    def __init__(self, username, password, admin=False):
        self.username = username
        self.password = generate_password_hash(password)
        self.admin = admin

    def __repr__(self):
        return f'<User id={self.id}; username={self.username}>'


class BlacklistToken(db.Model):
    '''Model for storing tokens that must no longer be valid'''
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<BlacklistedToken id={self.id}>'
