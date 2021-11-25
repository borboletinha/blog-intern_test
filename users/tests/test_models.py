from rest_framework.test import APITestCase
from django.contrib.auth import authenticate
from django.db.utils import DataError
from ..models import User


class UserTest(APITestCase):

    # Successful creation tests
    def test_user_creation(self):
        user = User.objects.create_user('Test_first_name', 'Test_last_name', 'Test_username',
                                        'test@email.blog', 'test_password123')
        self.assertIsInstance(user, User)
        self.assertEqual(user.first_name, 'Test_first_name')
        self.assertEqual(user.last_name, 'Test_last_name')
        self.assertEqual(user.username, 'Test_username')
        self.assertEqual(user.email, 'test@email.blog')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_user_password_hashing(self):
        User.objects.create_user('Test_first_name', 'Test_last_name', 'Test_username',
                                 'test@email.blog', 'test_password123')
        user = authenticate(email='test@email.blog', password='test_password123')
        self.assertIsNotNone(user)

    def test_superuser_creation(self):
        superuser = User.objects.create_superuser('Test_first_name', 'Test_last_name', 'Test_username',
                                                  'test@email.blog', 'test_password123')
        self.assertIsInstance(superuser, User)
        self.assertEqual(superuser.first_name, 'Test_first_name')
        self.assertEqual(superuser.last_name, 'Test_last_name')
        self.assertEqual(superuser.username, 'Test_username')
        self.assertEqual(superuser.email, 'test@email.blog')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_superuser_password_hashing(self):
        superuser = User.objects.create_superuser('Test_first_name', 'Test_last_name', 'Test_username',
                                                  'test@email.blog', 'test_password123')
        superuser = authenticate(email='test@email.blog', password='test_password123')
        self.assertIsNotNone(superuser)

    # Max length error tests
    def test_error_first_name_max_length(self):
        self.assertRaises(DataError, User.objects.create_user, first_name='_' * 256,
                          last_name='Test_last_name', username='Test_username',
                          email='test@email.blog', password='test_password123')

    def test_error_last_name_max_length(self):
        self.assertRaises(DataError, User.objects.create_user, first_name='Test_first_name',
                          last_name='_' * 256, username='Test_username',
                          email='test@email.blog', password='test_password123')

    def test_error_username_max_length(self):
        self.assertRaises(DataError, User.objects.create_user, first_name='Test_first_name',
                          last_name='Test_last_name', username='_' * 256,
                          email='test@email.blog', password='test_password123')

    # Not providing credentials tests
    def test_error_when_firstname_not_provided(self):
        self.assertRaises(ValueError, User.objects.create_user, first_name='',
                          last_name='Test_last_name', username='Test_username',
                          email='test@email.blog', password='test_password123')
        self.assertRaisesMessage(ValueError, 'Please enter your first name')

    def test_error_when_lastname_not_provided(self):
        self.assertRaises(ValueError, User.objects.create_user, first_name='Test_first_name',
                          last_name='', username='Test_username',
                          email='test@email.blog', password='test_password123')
        self.assertRaisesMessage(ValueError, 'Please enter your last name')

    def test_error_when_username_not_provided(self):
        self.assertRaises(ValueError, User.objects.create_user, first_name='Test_first_name',
                          last_name='Test_last_name', username='',
                          email='test@email.blog', password='test_password123')
        self.assertRaisesMessage(ValueError, 'Please enter your username')

    def test_error_when_email_not_provided(self):
        self.assertRaises(ValueError, User.objects.create_user, first_name='Test_first_name',
                          last_name='Test_last_name', username='Test_username',
                          email='', password='test_password123')
        self.assertRaisesMessage(ValueError, 'Please enter your email')

    def test_error_when_password_not_provided(self):
        self.assertRaises(ValueError, User.objects.create_user, first_name='Test_first_name',
                          last_name='Test_last_name', username='Test_username',
                          email='test@email.blog', password='')
        self.assertRaisesMessage(ValueError, 'Please enter your password')

    # Other
    def test_instance_name(self):
        user = User.objects.create_superuser('Test_first_name', 'Test_last_name', 'Test_username',
                                             'test@email.blog', 'test_password123')
        self.assertEqual(user.__str__(), 'Test_username|test@email.blog')
