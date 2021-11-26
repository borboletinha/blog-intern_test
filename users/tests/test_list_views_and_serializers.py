from collections import OrderedDict
from .test_setup import TestSetUp
from ..models import User


# DISPLAY OF USERS LISTS TESTS

class UsersUnsortedListViewsTest(TestSetUp):

    # Successful display of an unsorted users list
    def test_of_users_list_successful_display(self):
        user_1 = User.objects.create_user('Test_first_name', 'Test_last_name', 'Test_username1',
                                          'test@email.blog1', 'test_password123')

        user_2 = User.objects.create_user('Test_first_name', 'Test_last_name', 'Test_username2',
                                          'test@email.blog2', 'test_password123')

        user_3 = User.objects.create_user('Test_first_name', 'Test_last_name', 'Test_username3',
                                          'test@email.blog3', 'test_password123')
        database_user_1 = User.objects.values('id', 'first_name',
                                              'last_name', 'username').get(username='Test_username1')
        database_user_2 = User.objects.values('id', 'first_name',
                                              'last_name', 'username').get(username='Test_username2')
        database_user_3 = User.objects.values('id', 'first_name',
                                              'last_name', 'username').get(username='Test_username3')
        response = self.client.get(self.users_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0], OrderedDict(database_user_1))
        self.assertEqual(response.data[1], OrderedDict(database_user_2))
        self.assertEqual(response.data[2], OrderedDict(database_user_3))

    # No users list display
    def test_list_display_with_no_user(self):
        response = self.client.get(self.users_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    # GET method test
    def test_method_post_not_allowed(self):
        user_1 = User.objects.create_user('Test_first_name', 'Test_last_name', 'Test_username1',
                                          'test@email.blog1', 'test_password123')

        user_2 = User.objects.create_user('Test_first_name', 'Test_last_name', 'Test_username2',
                                          'test@email.blog2', 'test_password123')

        user_3 = User.objects.create_user('Test_first_name', 'Test_last_name', 'Test_username3',
                                          'test@email.blog3', 'test_password123')
        response = self.client.post(self.users_list_url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.data, {"detail": 'Method \"POST\" not allowed.'})


class UsersSortedListViewsTest(TestSetUp):

    # Successful display of an users list sorted by number of posts
    def test_of_sorted_users_list_successful_display(self):
        user_1 = User.objects.create_user('Test_first_name', 'Test_last_name', 'Test_username1',
                                          'test@email.blog1', 'test_password123')

        user_2 = User.objects.create_user('Test_first_name', 'Test_last_name', 'Test_username2',
                                          'test@email.blog2', 'test_password123')

        user_3 = User.objects.create_user('Test_first_name', 'Test_last_name', 'Test_username3',
                                          'test@email.blog3', 'test_password123')
        database_user_1 = User.objects.values('id', 'first_name',
                                              'last_name', 'username').get(username='Test_username1')
        database_user_2 = User.objects.values('id', 'first_name',
                                              'last_name', 'username').get(username='Test_username2')
        database_user_3 = User.objects.values('id', 'first_name',
                                              'last_name', 'username').get(username='Test_username3')
        response_u2 = self.client.post(self.login_url,
                                       {'email': 'test@email.blog2', 'password': 'test_password123'},
                                       format='json')
        access_token_u2 = response_u2.data['access']
        response_u3 = self.client.post(self.login_url,
                                    {'email': 'test@email.blog3', 'password': 'test_password123'},
                                    format='json')
        access_token_u3 = response_u3.data['access']
        user_3_post_1 = self.client.post(self.blogposts_create_url, {'title': 'Title1', 'text': 'Text'},
                                         HTTP_AUTHORIZATION=f'Bearer {access_token_u3}')
        user_3_post_2 = self.client.post(self.blogposts_create_url, {'title': 'Title2', 'text': 'Text'},
                                         HTTP_AUTHORIZATION=f'Bearer {access_token_u3}')
        user_2_post = self.client.post(self.blogposts_create_url, {'title': 'Title1', 'text': 'Text'},
                                       HTTP_AUTHORIZATION=f'Bearer {access_token_u2}')
        self.assertEqual(user_3_post_1.status_code, 201)
        self.assertEqual(user_3_post_2.status_code, 201)
        self.assertEqual(user_2_post.status_code, 201)
        response = self.client.get(self.users_sorted_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0], OrderedDict(database_user_3))
        self.assertEqual(response.data[1], OrderedDict(database_user_2))
        self.assertEqual(response.data[2], OrderedDict(database_user_1))

    # No users list display
    def test_list_display_with_no_user(self):
        response = self.client.get(self.users_sorted_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    # GET method test
    def test_method_post_not_allowed(self):
        user_1 = User.objects.create_user('Test_first_name', 'Test_last_name', 'Test_username1',
                                          'test@email.blog1', 'test_password123')

        user_2 = User.objects.create_user('Test_first_name', 'Test_last_name', 'Test_username2',
                                          'test@email.blog2', 'test_password123')

        user_3 = User.objects.create_user('Test_first_name', 'Test_last_name', 'Test_username3',
                                          'test@email.blog3', 'test_password123')
        response = self.client.post(self.users_sorted_list_url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.data, {"detail": 'Method \"POST\" not allowed.'})
