from flask_blog import ma
from flask_blog.users.models import User


class UserDetailSerializer(ma.SQLAlchemySchema):
    '''Schema for User detail serialization'''

    class Meta:
        model = User
        fields = ('id', 'username', 'admin', 'registered_on')
