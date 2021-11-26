from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUp(APITestCase):
    def setUp(self):
        # URLs
        self.create_url = reverse('blogposts_api:create')
        self.blogpost_url = reverse('blogposts_api:blogpost_detail')

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
