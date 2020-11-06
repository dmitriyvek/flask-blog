from flask_blog import db


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_on = db.Column(
        db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    author_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='cascade'), nullable=False)
    author = db.relationship('User', backref=db.backref(
        'post_list', lazy=True, cascade="all,delete-orphan"))

    def __repr__(self):
        return f'<Post id={self.id}; title={self.title}; author_id={self.author_id}>'
