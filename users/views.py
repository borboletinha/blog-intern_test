from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.db.models import Count
from .serializers import *
from .models import User


@swagger_auto_schema(method='post',
                     operation_description='Takes a set of the new user credentials, registers the user and returns '
                                           'confirmation that the user has just been successfully registered if '
                                           'all the necessary credentials have been provided and they are valid. '
                                           'Available only to unauthorized users.',
                     request_body=RegistrationSerializer,
                     responses={201: SwaggerRegistrationSerializer(many=True)}
                     )
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
    @swagger_auto_schema(operation_description='Displays all currently active users in unsorted order. '
                                               'Available to both authorized and unauthorized users.',
                         responses={200: UserSerializer(many=True)}
                         )
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class UsersSortedViewSet(viewsets.ViewSet):
    @swagger_auto_schema(operation_description='Displays all currently active users ordered by number of posts. '
                                               'Available to both authorized and unauthorized users.',
                         responses={200: UserSerializer(many=False)}
                         )
    def sorted_list(self, request):
        queryset = User.objects.all().annotate(num_posts=Count('blogpost')).order_by('-num_posts')
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


# JWT views for Swagger
class MyTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(operation_description='Takes a set of user credentials and returns an access and refresh JSON '
                                               'web token pair to prove the authentication of those credentials. '
                                               'Available only to unauthorized users.',
                         responses={200: SwaggerTokenObtainPairSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class MyTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(operation_description='Takes a refresh type JSON web token and returns an access type JSON web'
                                               'token if the refresh token is valid. '
                                               'Available only to authorized users.',
                         responses={200: SwaggerTokenRefreshSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
