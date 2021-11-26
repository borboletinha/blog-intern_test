from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUp(APITestCase):
    def setUp(self):
        # URLs
        self.create_url = reverse('blogposts_api:create')
        self.login_url = reverse('users_api:login')

        # Blogposts data
        self.post_data = {'title': 'Test_title', 'text': 'Test_text'}

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
