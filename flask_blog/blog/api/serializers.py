from marshmallow import fields, validate

from flask_blog import ma
from flask_blog.blog.models import Post


class PostDetailSerializer(ma.SQLAlchemySchema):
    '''Schema for Post detail serialization'''

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created_on',
                  'updated_on', 'author_id')


class PostCreationSerializer(ma.SQLAlchemySchema):
    '''Schema for Post creation input validation'''

    class Meta:
        model = Post
        fields = ('title', 'content')

    title = fields.Str(required=True, validate=validate.Length(min=1))
