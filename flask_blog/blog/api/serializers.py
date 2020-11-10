from flask_blog import ma
from flask_blog.blog.models import Post


class PostDetailSerializer(ma.SQLAlchemySchema):
    '''Schema for Post detail serialization'''

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created_on',
                  'updated_on', 'author_id')
