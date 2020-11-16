from marshmallow import fields, validate

from flask_blog import ma
from flask_blog.blog.api.serializers import PostListSerializer
from flask_blog.users.models import User


class UserDetailSerializer(ma.SQLAlchemySchema):
    '''Schema for User detail serialization'''

    class Meta:
        model = User
        fields = ('id', 'username', 'post_list')

    post_list = fields.Nested(PostListSerializer, many=True)


class UserCreationSerializer(ma.SQLAlchemySchema):
    '''Schema for User creation input validation'''

    class Meta:
        model = User
        fields = ('username', 'password')

    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=6))
