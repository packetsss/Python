""" 
run tests ignore venv folder
coverage run --omit="*/venv/* manage.py test
"""

from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from blog.models import Post, Category
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class PostTests(APITestCase):
    def test_view_posts(self):
        # get url from names
        url = reverse("blog_api:listcreate")

        # simulating browser using client
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        self.test_category = Category.objects.create(name="Test Category")
        self.test_user_1 = User.objects.create_superuser(
            username="test_user_1", password="123123123"
        )
        self.client.login(username=self.test_user_1.username, password="123123123")
        url = reverse("blog_api:listcreate")

        data = {"title": "new", "author": 1, "excerpt": "new", "content": "new"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 6)

        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # test custom permission
    def test_post_update(self):
        client = APIClient()

        self.test_category = Category.objects.create(name="django")
        self.testuser1 = User.objects.create_user(
            username="test_user1", password="123456789"
        )
        self.testuser2 = User.objects.create_user(
            username="test_user2", password="123456789"
        )
        test_post = Post.objects.create(
            category_id=1,
            title="Post Title",
            excerpt="Post Excerpt",
            content="Post Content",
            slug="post-title",
            author_id=1,
            status="published",
        )

        client.login(username=self.testuser1.username, password="123456789")

        url = reverse(("blog_api:detailcreate"), kwargs={"pk": 1})

        response = client.put(
            url,
            {
                "title": "New",
                "author": 1,
                "excerpt": "New",
                "content": "New",
                "status": "published",
            },
            format="json",
        )
        print(response.data)  # see detail failure
        self.assertEqual(response.status_code, status.HTTP_200_OK)
