from marshmallow import fields, validate

from flask_blog import ma
from flask_blog.blog.api.serializers import PostListSerializer
from flask_blog.users.models import User


class UserDetailSerializer(ma.SQLAlchemySchema):
    '''Schema for User detail serialization'''

    class Meta:
        model = User
        fields = ('id', 'username', 'posts')

    posts = fields.Nested(PostListSerializer, many=True)


class UserCreationSerializer(ma.SQLAlchemySchema):
    '''Schema for User creation input validation'''

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    username = fields.Str(required=True, validate=validate.Length(
        min=4, error='Username is to short. Must be more than 4 chars long'))
    email = fields.Str(
        required=False, validate=validate.Email(error='Not a valid email address')
    )
    password = fields.Str(required=True, validate=validate.Length(
        min=6, error='Password is to short. Must be more than 6 chars long'))
