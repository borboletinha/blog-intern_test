from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import IntegrityError
from .models import BlogPost
from .serializers import BlogPostSerializer


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
