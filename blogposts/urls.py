from django.urls import path
from .views import *


app_name = 'blogposts_api'
urlpatterns = [
    path('create/', blogpost_creation_view, name='create'),
    path('<slug>/', blogpost_detail_view, name='blogpost_detail'),
]
