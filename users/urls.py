from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *


app_name = 'users_api'
users_list = UsersViewSet.as_view({'get': 'list'})
users_list_sorted = UsersSortedViewSet.as_view({'get': 'retrieve'})
urlpatterns = [
    path('register/', registration_view, name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login_token_refresh'),
    path('all/', users_list, name='users_list'),
    path('all/sorted/', users_list_sorted, name='users_list_sorted'),
]
