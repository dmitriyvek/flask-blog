import json
from datetime import datetime

from flask import abort,  make_response, jsonify

from flask_blog import db
from flask_blog.blog.models import Post
from flask_blog.users.models import User


def check_if_post_is_already_exist(title: str) -> None:
    '''Check if post with the given title is already exists. Aborts 400 Response if it does.'''
    post = Post.query.filter_by(title=title).first()
    if post:
        error_message = {
            'status': 'fail',
            'message': 'Post with given title is already exist.',
        }
        abort(make_response(jsonify(error_message), 400))


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


def check_if_user_is_post_author(user_id: int, post_id: dict) -> Post:
    '''Checks if request user is the author of the given Post. If he does then returns this Post, if he does not then abort 403 Response'''
    post = Post.query.get_object_or_404(id=post_id)

    if post.author_id != user_id:
        error_message = {
            'status': 'fail',
            'message': 'You are not allowed to change this resource.'
        }
        abort(make_response(jsonify(error_message), 403))

    return post


def update_and_return_post(post: Post, data: dict) -> Post:
    '''Updates and returns given Post'''
    if data.get('title'):
        if post.title != data['title']:
            check_if_post_is_already_exist(data['title'])
            post.title = data['title']

    if data.get('content'):
        post.content = data['content']

    post.updated_on = datetime.now()
    db.session.commit()
    return post


def mark_post_as_deleted(post: Post) -> None:
    '''Set Post.is_deleted to True'''
    post.is_deleted = True
    db.session.commit()
