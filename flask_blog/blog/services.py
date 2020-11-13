import json

from flask import Response, abort

from flask_blog import db
from flask_blog.blog.models import Post
from flask_blog.users.models import User


def check_if_post_is_already_exist(data: dict) -> None:
    '''Check if post with the given title is already exists. Aborts 400 Response if it does.'''
    post = Post.query.filter_by(title=data['title']).first()
    if post:
        error_message = json.dumps({
            'status': 'fail',
            'message': 'Post with given title is already exist.',
        })
        abort(Response(error_message, 400))


def create_and_return_new_post(data: dict, author_id: int) -> Post:
    '''Creates and returns new Post with given data and author'''
    author = User.query.get(author_id)
    post = Post(
        title=data['title'],
        content=data['content'],
        author=author
    )

    db.session.add(post)
    db.session.commit()

    return post
