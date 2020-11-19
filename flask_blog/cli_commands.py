import click
from flask.cli import with_appcontext

from flask_blog import db
from flask_blog.blog.models import Post
from flask_blog.users.models import User


@click.command('init_db_data')
@with_appcontext
def init_db_data():
    user1 = User(username='admin', password='zxcfghuio')
    user2 = User(username='admin2', password='zxcfghuio')
    user3 = User(username='admin3', password='zxcfghuio')

    for i in range(9):
        author = user1 if i % 3 == 0 else user2 if i % 3 == 1 else user3
        Post(title=f'test_title_{i+1}',
             content=f'test_content_{i+1}',
             author=author
             )
    Post(title='deleted_post', author=user1, is_deleted=True)

    db.session.add_all([user1, user2, user3])
    db.session.commit()
    click.echo('Initialized the database data.')
