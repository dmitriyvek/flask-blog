from flask_blog.users.models import User


class UserDetailSerializer:
    '''Some dummy user serializer'''

    def __init__(self, user_id: int):
        user = User.query.filter_by(id=user_id).first()
        self.data: dict = {
            'user_id': user.id,
            'username': user.username,
            'admin': user.admin,
            'registered_on': user.registered_on
        }
