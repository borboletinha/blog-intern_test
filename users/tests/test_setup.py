from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUp(APITestCase):
    def setUp(self):
        # URLs
        self.register_url = reverse('users_api:register')
        self.login_url = reverse('users_api:login')
        self.login_refresh_url = reverse('users_api:login_token_refresh')
        self.users_list_url = reverse('users_api:users_list')
        self.users_sorted_list_url = reverse('users_api:users_list_sorted')
        self.blogposts_create_url = reverse('blogposts_api:create')

        # Users data
        self.user_data1 = {'first_name': 'Test_first_name', 'last_name': 'Test_last_name',
                           'username': 'Test_username', 'email': 'test@email.blog', 'password': 'test_password123',
                           'confirmed_password': 'test_password123'}
        self.user_data2 = {'first_name': 'Test_first_name', 'last_name': 'Test_last_name',
                           'username': 'Test_username', 'email': 'test@email.blogXXX', 'password': 'test_password123',
                           'confirmed_password': 'test_password123'}
        self.user_data3 = {'first_name': 'Test_first_name', 'last_name': 'Test_last_name',
                           'username': 'Test_usernameXXX', 'email': 'test@email.blog', 'password': 'test_password123',
                           'confirmed_password': 'test_password123'}
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
