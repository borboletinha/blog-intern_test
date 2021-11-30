from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from .models import BlogPost
from .serializers import *


@swagger_auto_schema(method='post',
                     operation_description='Takes a set of the new post data, creates the post and returns '
                                           'the data that the post has just been successfully published if '
                                           'all the necessary data has been provided and it is valid. ' 
                                           'Available only to authorized users.',
                     request_body=BlogPostSerializer,
                     responses={201: SwaggerBlogPostCreationSerializer(many=True)}
                     )
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def blogpost_creation_view(request):
    author = request.user
    blogpost = BlogPost(author=author)
    serializer = BlogPostSerializer(blogpost, data=request.data)
    if serializer.is_valid():
        try:
            post = serializer.save()
        except IntegrityError:
            return Response({'detail': 'You have already used the title'},
                            status=status.HTTP_400_BAD_REQUEST)
        data = {'slug': post.slug, 'title': post.title, 'text': post.text,
                'first_name': post.author.first_name, 'last_name': post.author.last_name,
                'username': post.author.username}
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = serializer.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get',
                     operation_description='Displays all information about a particular post. ' 
                                           'Available to both authorized and unauthorized users.',
                     responses={200: BlogPostSerializer(many=True)}
                     )
@api_view(['GET'])
@permission_classes([AllowAny])
def blogpost_detail_view(request, slug):
    try:
        blogpost = BlogPost.objects.get(slug=slug)
    except BlogPost.DoesNotExist:
        return Response({'detail': "The post doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
    serializer = BlogPostSerializer(blogpost)
    data = serializer.data
    return Response(data)
