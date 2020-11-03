from app import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_on = db.Column(
        db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                          nullable=False)
    author = db.relationship('User',
                             backref=db.backref('post_list', lazy=True))

    def __repr__(self):
        return f'<Post {self.title}>'
