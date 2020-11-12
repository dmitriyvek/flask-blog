from flask_blog import db


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), comment='DateTime of post creation')
    updated_on = db.Column(
        db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), comment='DateTime of post update')
    is_deleted = db.Column(db.Boolean, nullable=False, default=False,
                           comment='If the post is marked for deletion then it should not be given to the client')

    author_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='cascade'), nullable=False)
    author = db.relationship('User', backref=db.backref(
        'post_list', lazy=True, cascade="all,delete-orphan"))

    def __repr__(self):
        return f'<Post id={self.id}; title={self.title}; author_id={self.author_id}>'
