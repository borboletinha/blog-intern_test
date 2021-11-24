from django.core.exceptions import ValidationError
from django.urls import reverse
from .test_setup import TestSetUp
from ..models import User


class RegistrationViewsTest(TestSetUp):

    # Registration without credentials tests
    def test_of_user_cannot_register_without_all_credentials(self):
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, 400)
        self.assertRaisesMessage(ValidationError, {"success": False, "response": "The user isn't created.",
                                                   "first_name": ["This field is required."],
                                                   "last_name": ["This field is required."],
                                                   "username": ["This field is required."],
                                                   "email": ["This field is required."],
                                                   "password": ["This field is required."],
                                                   "confirmed_password": ["This field is required."]})

    def test_of_user_cannot_register_without_first_name(self):
        response = self.client.post(self.register_url, {'first_name': '', 'last_name': 'Test_last_name',
                                                        'username': 'Test_username', 'email': 'test@email.blog',
                                                        'password': 'test_password123',
                                                        'confirmed_password': 'test_password123'})
        self.assertEqual(response.status_code, 400)
        self.assertRaisesMessage(ValidationError, {"success": False, "response": "The user isn't created.",
                                                   "first_name": ["This field is required."]})

    def test_of_user_cannot_register_without_last_name(self):
        response = self.client.post(self.register_url, {'first_name': 'Test_first_name', 'last_name': '',
                                                        'username': 'Test_username', 'email': 'test@email.blog',
                                                        'password': 'test_password123',
                                                        'confirmed_password': 'test_password123'})
        self.assertEqual(response.status_code, 400)
        self.assertRaisesMessage(ValidationError, {"success": False, "response": "The user isn't created.",
                                                   "last_name": ["This field is required."]})

    def test_of_user_cannot_register_without_username(self):
        response = self.client.post(self.register_url, {'first_name': 'Test_first_name', 'last_name': 'Test_last_name',
                                                        'username': '', 'email': 'test@email.blog',
                                                        'password': 'test_password123',
                                                        'confirmed_password': 'test_password123'})
        self.assertEqual(response.status_code, 400)
        self.assertRaisesMessage(ValidationError, {"success": False, "response": "The user isn't created.",
                                                   "username": ["This field is required."]})

    def test_of_user_cannot_register_without_email(self):
        response = self.client.post(self.register_url, {'first_name': 'Test_first_name', 'last_name': 'Test_last_name',
                                                        'username': 'Test_username', 'email': '',
                                                        'password': 'test_password123',
                                                        'confirmed_password': 'test_password123'})
        self.assertEqual(response.status_code, 400)
        self.assertRaisesMessage(ValidationError, {"success": False, "response": "The user isn't created.",
                                                   "email": ["This field is required."]})

    def test_of_user_cannot_register_without_password(self):
        response = self.client.post(self.register_url, {'first_name': 'Test_first_name', 'last_name': 'Test_last_name',
                                                        'username': 'Test_username', 'email': 'test@email.blog',
                                                        'password': '',
                                                        'confirmed_password': 'test_password123'})
        self.assertEqual(response.status_code, 400)
        self.assertRaisesMessage(ValidationError, {"success": False, "response": "The user isn't created.",
                                                   "password": ["This field is required."]})

    def test_of_user_cannot_register_without_confirmed_password(self):
        response = self.client.post(self.register_url,
                                    {'first_name': 'Test_first_name', 'last_name': 'Test_last_name',
                                     'username': 'Test_username', 'email': 'test@email.blog',
                                     'password': 'test_password123',
                                     'confirmed_password': ''})
        self.assertEqual(response.status_code, 400)
        self.assertRaisesMessage(ValidationError, {"success": False, "response": "The user isn't created.",
                                                   "confirmed_password": ["This field is required."]})

    # Correct registration test
    def test_of_user_successfully_register(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {"success": True, "response": "The user is successfully created.",
                                         'first_name': 'Test_first_name', 'last_name': 'Test_last_name',
                                         'username': 'Test_username', 'email': 'test@email.blog'})

    # Registration with preexisting unique credentials
    def test_of_user_with_preexisted_username(self):
        init_response = self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.register_url, self.user_data2, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"success": False, "response": "The user isn't created.",
                                         "username": ["user with this username already exists."]})

    def test_of_user_with_preexisted_email(self):
        init_response = self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.register_url, self.user_data3, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"success": False, "response": "The user isn't created.",
                                         "email": ["user with this email already exists."]})


class LogInViewsTest(TestSetUp):
    def test_successful_log_in(self):
        user = User.objects.create_user('Test_first_name', 'Test_last_name', 'Test_username',
                                        'test@email.blog', 'test_password123')
        user.save()

        response = self.client.post(self.login_url,
                                    {'email': 'test@email.blog', 'password': 'test_password123'},
                                    format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('refresh' in response.data)
        self.assertTrue('access' in response.data)
