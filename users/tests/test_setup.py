from rest_framework.test import APITestCase, APIClient
from django.urls import reverse


class TestSetUp(APITestCase):
    def setUp(self):
        self.register_url = reverse('users_api:register')
        self.login_url = reverse('users_api:login')
        self.login_refresh_url = reverse('users_api:login_token_refresh')
        self.user_data = {'first_name': 'Test_first_name', 'last_name': 'Test_last_name',
                          'username': 'Test_username', 'email': 'test@email.blog', 'password': 'test_password123',
                          'confirmed_password': 'test_password123'}
        self.user_data2 = {'first_name': 'Test_first_name', 'last_name': 'Test_last_name',
                           'username': 'Test_username', 'email': 'test2@email.blog', 'password': 'test_password123',
                           'confirmed_password': 'test_password123'}
        self.user_data3 = {'first_name': 'Test_first_name3', 'last_name': 'Test_last_name',
                           'username': 'Test_username3', 'email': 'test@email.blog', 'password': 'test_password123',
                           'confirmed_password': 'test_password123'}
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
