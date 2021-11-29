from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from django.db.models import Count
from .serializers import *
from .models import User


@api_view(['POST'])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        data = {'detail': 'The user is successfully created.',
                'first_name': user.first_name, 'last_name': user.last_name,
                'username': user.username, 'email': user.email}
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = {'detail': "The user isn't created."}
        data.update(serializer.errors)
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class UsersSortedViewSet(viewsets.ViewSet):
    def sorted_list(self, request):
        queryset = User.objects.all().annotate(num_posts=Count('blogpost')).order_by('-num_posts')
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
