
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    number_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'text', 'link', 'number_likes')
        read_only_fields = ('id', 'number_likes', )

    def get_number_likes(self, post):
        return post.likes.count()
