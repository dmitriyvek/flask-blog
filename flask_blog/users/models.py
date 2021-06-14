from werkzeug.security import generate_password_hash

from flask_blog import db


class User(db.Model):
    '''
    The common model used for stored inforamtion about users.
    '''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        comment='Username used for authentication'
    )
    email = db.Column(
        db.String(255),
        unique=True,
        nullable=True,
        comment='Email used for account confirmation and password reset'
    )
    is_confirmed = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        comment='Is user email (and so account) confirmed'
    )
    password = db.Column(
        db.Text,
        nullable=False,
        comment='Hashed user password'
    )
    registered_on = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        comment='DateTime of registration'
    )
    admin = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        comment='Does user has admin privileges'
    )
    is_deleted = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        comment='If the user is marked for deletion then '
        'it should not be valid for authentification'
    )

    # post_list = db.relationship('Post', backref=db.backref(
    #     'author'), cascade="all, delete")

    def __init__(self, username, password, admin=False, email=None):
        self.username = username
        self.email = email
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
