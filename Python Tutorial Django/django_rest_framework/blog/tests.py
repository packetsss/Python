""" 
run tests ignore venv folder
coverage run --omit="*/venv/* manage.py test
"""

from django.test import TestCase
from blog.models import Post, Category
from django.contrib.auth.models import User

# test on using api
class TestCreatePost(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_category = Category.objects.create(name="new_category")
        test_category.save()
        test_user_1 = User.objects.create_user(
            username="test_user_1", password="12314134"
        )
        test_user_1.save()
        test_post = Post.objects.create(
            category_id=1,
            title="Post Title",
            excerpt="Post Excerpt",
            content="Post Content",
            slug="post-title",
            author_id=1,
            status="published",
        )
        test_post.save()

    def test_blog_content(self):
        post = Post.post_objects.get(id=1)
        cat = Category.objects.get(id=1)
        author = f"{post.author}"
        excerpt = f"{post.excerpt}"
        title = f"{post.title}"
        content = f"{post.content}"
        status = f"{post.status}"
        self.assertEqual(author, "test_user_1")
        self.assertEqual(title, "Post Title")
        self.assertEqual(content, "Post Content")
        self.assertEqual(status, "published")
        self.assertEqual(str(post), "Post Title")
        self.assertEqual(str(cat), "new_category")
