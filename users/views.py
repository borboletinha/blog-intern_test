from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import RegistrationSerializer


@api_view(['POST'])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        data = {'success': True, 'response': 'The user is successfully created',
                'first_name': user.first_name, 'last_name': user.last_name,
                'username': user.username, 'email': user.email}
    else:
        data = {'success': False, 'response': "The user isn't created'"}
        data.update(serializer.errors)
    return Response(data, status=status.HTTP_201_CREATED)
