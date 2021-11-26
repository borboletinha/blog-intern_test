from django.core.exceptions import ValidationError
from django.urls import reverse
from .test_setup import TestSetUp
from users.models import User


# BLOGPOSTS CREATION AND DISPLAY TESTS
from ..models import BlogPost


class PostCreationViewTest(TestSetUp):

    def setup(self):
        user = User.objects.create_user('Test_first_name', 'Test_last_name', 'Test_username',
                                        'test@email.blog', 'test_password123')
        response = self.client.post(self.login_url,
                                    {'email': 'test@email.blog', 'password': 'test_password123'},
                                    format='json')
        return response.data['access']

    # Successful blogpost creation test
    def test_post_creation(self):
        access_token = PostCreationViewTest.setup(self)
        response = self.client.post(self.create_url, self.post_data,
                                    HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {'success': True, 'slug': 'test_username-test_title',
                                         'title': 'Test_title', 'text': 'Test_text',
                                         'first_name': 'Test_first_name', 'last_name': 'Test_last_name',
                                         'username': 'Test_username'})

    # Max length error tests
    def test_error_title_max_length(self):
        access_token = PostCreationViewTest.setup(self)
        response = self.client.post(self.create_url, {'title': '_' * 301, 'text': 'Test_text'},
                                    HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertRaisesMessage(ValidationError, {"title": ["Ensure this field has no more than 3 characters."]})

    def test_error_text_max_length(self):
        access_token = PostCreationViewTest.setup(self)
        response = self.client.post(self.create_url, {'title': '_' * 7001, 'text': 'Test_text'},
                                    HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertRaisesMessage(ValidationError, {"text": ["Ensure this field has no more than 3 characters."]})

    # Post creation without required information tests
    def test_post_cannot_be_created_without_title(self):
        access_token = PostCreationViewTest.setup(self)
        response = self.client.post(self.create_url, {'title': '', 'text': 'Test_text'},
                                    HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertRaisesMessage(ValidationError, {"title": ["This field may not be blank."]})

    def test_post_cannot_be_created_without_text(self):
        access_token = PostCreationViewTest.setup(self)
        response = self.client.post(self.create_url, {'title': 'Test_title', 'text': ''},
                                    HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertRaisesMessage(ValidationError, {"text": ["This field may not be blank."]})

    def test_post_cannot_be_created_without_text_and_title(self):
        access_token = PostCreationViewTest.setup(self)
        response = self.client.post(self.create_url, {'title': '', 'text': ''},
                                    HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 400)
        self.assertRaisesMessage(ValidationError, {"title": ["This field may not be blank."],
                                                   "text": ["This field may not be blank."]})

    # Post creation without access token test
    def test_post_cannot_be_created_without_token(self):
        access_token = PostCreationViewTest.setup(self)
        response = self.client.post(self.create_url, self.post_data)
        self.assertEqual(response.status_code, 401)
        self.assertRaisesMessage(ValidationError, {"detail": "Authentication credentials were not provided."})

    # Post creation with bad access token test
    def test_post_cannot_be_created_with_bad_token(self):
        access_token = PostCreationViewTest.setup(self)
        response = self.client.post(self.create_url, self.post_data,
                                    HTTP_AUTHORIZATION=f'Bearer {"bad_token"}')
        self.assertEqual(response.status_code, 401)
        self.assertRaisesMessage(ValidationError, {"detail": "Given token not valid for any token type",
                                                   "code": "token_not_valid",
                                                   "messages": [{"token_class": "AccessToken", "token_type": "access",
                                                                 "message": "Token is invalid or expired"}]})

    # Post creation with preexisting title
    def test_of_post_creation_with_preexisting_title(self):
        access_token = PostCreationViewTest.setup(self)
        response_1 = self.client.post(self.create_url, self.post_data,
                                      HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response_2 = self.client.post(self.create_url, self.post_data,
                                      HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response_2.status_code, 400)
        self.assertEqual(response_2.data, {'success': False, 'response': 'You have already used the title'})

    # GET method test
    def test_method_get_not_allowed(self):
        access_token = PostCreationViewTest.setup(self)
        response = self.client.get(self.create_url, self.post_data,
                                   HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.data, {"detail": 'Method \"GET\" not allowed.'})


class PostDisplayViewTest(TestSetUp):

    def setup(self):
        user = User.objects.create_user('Test_first_name', 'Test_last_name', 'Test_username',
                                        'test@email.blog', 'test_password123')
        response = self.client.post(self.login_url,
                                    {'email': 'test@email.blog', 'password': 'test_password123'},
                                    format='json')
        access_token = response.data['access']

        return self.client.post(self.create_url, self.post_data,
                                HTTP_AUTHORIZATION=f'Bearer {access_token}')

    # Successful blogpost display test
    def test_post_display_unauthorized(self):
        post_response = PostDisplayViewTest.setup(self)
        blogpost = BlogPost.objects.get(slug=post_response.data['slug'])
        self.assertEqual(post_response.data['slug'], 'test_username-test_title')
        response = self.client.get(reverse('blogposts_api:blogpost_detail',
                                           kwargs={'slug': post_response.data['slug']}), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'success': True, 'title': 'Test_title', 'text': 'Test_text',
                                         'first_name': 'Test_first_name', 'last_name': 'Test_last_name',
                                         'username': 'Test_username'})

    def test_post_display_authorized(self):
        user = User.objects.create_user('Test_first_name', 'Test_last_name', 'Test_username',
                                        'test@email.blog', 'test_password123')
        response = self.client.post(self.login_url,
                                    {'email': 'test@email.blog', 'password': 'test_password123'},
                                    format='json')
        access_token = response.data['access']

        return self.client.post(self.create_url, self.post_data,
                                HTTP_AUTHORIZATION=f'Bearer {access_token}')
        blogpost = BlogPost.objects.get(slug=post_response.data['slug'])
        self.assertEqual(post_response.data['slug'], 'test_username-test_title')
        response = self.client.get(reverse('blogposts_api:blogpost_detail',
                                           kwargs={'slug': post_response.data['slug']}),
                                   HTTP_AUTHORIZATION=f'Bearer {access_token}', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'success': True, 'title': 'Test_title', 'text': 'Test_text',
                                         'first_name': 'Test_first_name', 'last_name': 'Test_last_name',
                                         'username': 'Test_username'})

    # Display of an nonexistent post set test
    def test_nonexistent_post_display(self):
        response = self.client.get(reverse('blogposts_api:blogpost_detail',
                                           kwargs={'slug': 'random_slug'}), format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {'success': False, 'response': "The post doesn't exist"})

    # POST method test
    def test_method_get_not_allowed(self):
        post_response = PostDisplayViewTest.setup(self)
        blogpost = BlogPost.objects.get(slug=post_response.data['slug'])
        self.assertEqual(post_response.data['slug'], 'test_username-test_title')
        response = self.client.post(
            reverse('blogposts_api:blogpost_detail', kwargs={'slug': post_response.data['slug']}), format='json')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.data, {"detail": 'Method \"POST\" not allowed.'})

