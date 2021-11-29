from rest_framework import serializers
from .models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField('get_first_name')
    last_name = serializers.SerializerMethodField('get_last_name')
    username = serializers.SerializerMethodField('get_username')

    def get_first_name(self, blogpost):
        first_name = blogpost.author.first_name
        return first_name

    def get_last_name(self, blogpost):
        last_name = blogpost.author.last_name
        return last_name

    def get_username(self, blogpost):
        username = blogpost.author.username
        return username

    class Meta:
        model = BlogPost
        fields = ['title', 'text', 'first_name',
                  'last_name', 'username']


# Serializers for Swagger

class SwaggerBlogPostCreationSerializer(serializers.Serializer):
    def get_first_name(self, blogpost):
        first_name = blogpost.author.first_name
        return first_name

    def get_last_name(self, blogpost):
        last_name = blogpost.author.last_name
        return last_name

    def get_username(self, blogpost):
        username = blogpost.author.username
        return username

    slug = serializers.SlugField()
    title = serializers.CharField()
    text = serializers.CharField()
    first_name = serializers.SerializerMethodField('get_first_name')
    last_name = serializers.SerializerMethodField('get_last_name')
    username = serializers.SerializerMethodField('get_username')
