from rest_framework.test import APITestCase
from django.db.utils import DataError
from users.models import User
from blogposts.models import BlogPost


class BlogPostTest(APITestCase):

    def setup(self):
        return User.objects.create_user('Test_first_name', 'Test_last_name', 'Test_username',
                                        'test@email.blog', 'test_password123')

    # Successful creation tests
    def test_blogpost_creation(self):
        user = BlogPostTest.setup(self)
        blogpost = BlogPost.objects.create(title='Test_title', text='Test_text', author=user)
        self.assertIsInstance(blogpost, BlogPost)
        self.assertEqual(blogpost.title, 'Test_title')
        self.assertEqual(blogpost.text, 'Test_text')
        self.assertEqual(blogpost.author.first_name, 'Test_first_name')
        self.assertEqual(blogpost.author.last_name, 'Test_last_name')
        self.assertEqual(blogpost.author.username, 'Test_username')

    # Max length error tests
    def test_error_title_max_length(self):
        user = BlogPostTest.setup(self)
        self.assertRaises(DataError, BlogPost.objects.create, title='_' * 301, text='Test_text', author=user)

    # URL tests
    def test_slug(self):
        user = BlogPostTest.setup(self)
        blogpost = BlogPost.objects.create(title='Test_title', text='Test_text', author=user)
        self.assertEqual(blogpost.slug, 'test_username-test_title')

    def test_absolute_url(self):
        user = BlogPostTest.setup(self)
        blogpost = BlogPost.objects.create(title='Test_title', text='Test_text', author=user)
        self.assertEqual(blogpost.get_absolute_url(), '/api/posts/test_username-test_title/')

    # Other
    def test_instance_name(self):
        user = BlogPostTest.setup(self)
        blogpost = BlogPost.objects.create(title='Test_title', text='Test_text', author=user)

        self.assertEqual(blogpost.__str__(), 'Test_title|Test_username')
