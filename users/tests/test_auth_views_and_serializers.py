from django.core.exceptions import ValidationError
from .test_setup import TestSetUp
from ..models import User


# USER REGISTRATION AND LOG IN TESTS


class RegistrationViewTest(TestSetUp):

    # Successful registration test
    def test_registration(self):
        response = self.client.post(self.register_url, self.user_data1, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {"success": True, "response": "The user is successfully created.",
                                         'first_name': 'Test_first_name', 'last_name': 'Test_last_name',
                                         'username': 'Test_username', 'email': 'test@email.blog'})

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

    # Registration with preexisting unique credentials
    def test_of_registration_with_preexisted_username(self):
        init_response = self.client.post(self.register_url, self.user_data1, format='json')
        response = self.client.post(self.register_url, self.user_data2, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"success": False, "response": "The user isn't created.",
                                         "username": ["user with this username already exists."]})

    def test_of_registration_with_preexisted_email(self):
        init_response = self.client.post(self.register_url, self.user_data1, format='json')
        response = self.client.post(self.register_url, self.user_data3, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"success": False, "response": "The user isn't created.",
                                         "email": ["user with this email already exists."]})

    # Mismatching passwords test
    def test_of_mismatching_between_password_and_confirmed_password(self):
        response = self.client.post(self.register_url, {'first_name': 'Test_first_name', 'last_name': 'Test_last_name',
                                                        'username': 'Test_username', 'email': 'test@email.blog',
                                                        'password': 'test_password123',
                                                        'confirmed_password': 'test_password000'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"password": "Please enter matched passwords."})

    # GET method test
    def test_method_get_not_allowed(self):
        response = self.client.get(self.register_url, self.user_data1, format='json')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.data, {"detail": 'Method \"GET\" not allowed.'})


class LogInViewsTest(TestSetUp):

    def setup(self):
        user = User.objects.create_user('Test_first_name', 'Test_last_name', 'Test_username',
                                        'test@email.blog', 'test_password123')

    # Successful log in tests
    def test_log_in(self):
        LogInViewsTest.setup(self)
        response = self.client.post(self.login_url,
                                    {'email': 'test@email.blog', 'password': 'test_password123'},
                                    format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('refresh' in response.data)
        self.assertTrue('access' in response.data)

    # Mismatching credentials tests
    def test_log_in_with_wrong_email(self):
        LogInViewsTest.setup(self)
        response = self.client.post(self.login_url,
                                    {'email': 'wrong@email.blog', 'password': 'test_password123'},
                                    format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {"detail": "No active account found with the given credentials"})

    def test_log_in_with_wrong_password(self):
        LogInViewsTest.setup(self)
        response = self.client.post(self.login_url,
                                    {'email': 'test@email.blog', 'password': 'test_password000'},
                                    format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {"detail": "No active account found with the given credentials"})

    def test_log_in_with_wrong_email_and_password(self):
        LogInViewsTest.setup(self)
        response = self.client.post(self.login_url,
                                    {'email': 'wrong@email.blog', 'password': 'test_password000'},
                                    format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {"detail": "No active account found with the given credentials"})

    # GET method test
    def test_method_get_not_allowed(self):
        LogInViewsTest.setup(self)
        response = self.client.get(self.register_url, self.user_data1, format='json')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.data, {"detail": 'Method \"GET\" not allowed.'})


class TokenRefreshTests(TestSetUp):

    def setup(self):
        user = User.objects.create_user('Test_first_name', 'Test_last_name', 'Test_username',
                                        'test@email.blog', 'test_password123')

    # Token refresh tests
    def test_token_refresh(self):
        TokenRefreshTests.setup(self)
        response = self.client.post(self.login_url,
                                    {'email': 'test@email.blog', 'password': 'test_password123'},
                                    format='json')
        refresh_token = response.data['refresh']
        response_refresh = self.client.post(self.login_refresh_url, {'refresh': refresh_token})
        self.assertEqual(response_refresh.status_code, 200)
        self.assertTrue('access' in response_refresh.data)

    def test_failed_token_refresh_with_wrong_refresh_token(self):
        TokenRefreshTests.setup(self)
        response = self.client.post(self.login_url,
                                    {'email': 'test@email.blog', 'password': 'test_password123'},
                                    format='json')
        refresh_token = response.data['refresh']
        self.assertNotEqual(refresh_token, 'wrong_test_token')
        response_refresh = self.client.post(self.login_refresh_url, {'refresh': 'wrong_test_token'})
        self.assertEqual(response_refresh.status_code, 401)
        self.assertTrue(response_refresh.data, {"detail": "Token has wrong type", "code": "token_not_valid"})

    # Token refresh without credentials test
    def test_failed_token_refresh_without_refresh_token(self):
        TokenRefreshTests.setup(self)
        response = self.client.post(self.login_url,
                                    {'email': 'test@email.blog', 'password': 'test_password123'},
                                    format='json')
        refresh_token = response.data['refresh']
        self.assertNotEqual(refresh_token, 'wrong_test_token')
        response_refresh = self.client.post(self.login_refresh_url, {'refresh': ''})
        self.assertEqual(response_refresh.status_code, 400)
        self.assertTrue(response_refresh.data, {"refresh": ["This field may not be blank."]})

    # GET method test
    def test_method_get_not_allowed(self):
        TokenRefreshTests.setup(self)
        response = self.client.get(self.login_url,
                                   {'email': 'test@email.blog', 'password': 'test_password123'},
                                   format='json')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.data, {"detail": 'Method \"GET\" not allowed.'})
