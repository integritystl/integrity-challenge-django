from datetime import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment
from django.core.files.uploadedfile import SimpleUploadedFile
from .models.Post import Status

# POST DATA
POST_TITLE = 'Test Post'
POST_CONTENT = 'Test content'

# COMMENT DATA
COMMENT_CONTENT = 'Test comment'

# USER DATA
USERNAME = 'testuser'
PASSWORD = 'testpass123'

# ADMIN USER DATA
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'
ADMIN_EMAIL = 'admin@test.com'


class BlogTests(TestCase):
    """
    Tests for post and comment creation / editing

    To run -> python manage.py test
    """
    def setUp(self):
        # CREATE USERS
        self.user = User.objects.create_user(
            username=USERNAME,
            password=PASSWORD
        )
        self.admin_user = User.objects.create_superuser(
            username=ADMIN_USERNAME,
            password=ADMIN_PASSWORD,
            email=ADMIN_EMAIL
        )

        # CREATE TEST POST
        self.post = Post.objects.create(
            title=POST_TITLE,
            content=POST_CONTENT,
            author=self.user,
            status=Status.published
        )

        # CREATE TEST COMMENT
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content=COMMENT_CONTENT
        )

        self.client = Client()

    def test_post_creation(self):
        """
        Test post was created
        """
        self.assertEqual(self.post.title, POST_TITLE)
        self.assertEqual(self.post.content, POST_CONTENT)
        self.assertEqual(self.post.author, self.user)
        self.assertTrue(isinstance(self.post.created_on, datetime))
        self.assertTrue(self.post.status == Status.published)

    def test_comment_creation(self):
        """
        Test comment was created and connected to the post and author
        """
        self.assertEqual(self.comment.content, COMMENT_CONTENT)
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.post.comments.count(), 1)

    def test_add_comment_authenticated(self):
        """
        Test adding a comment as an authenticated user
        """
        self.client.login(username=USERNAME, password=PASSWORD)
        self.client.post(
            reverse('blog:add_comment', kwargs={'post_id': self.post.id}),
            {'content': 'New test comment'}
        )
        self.assertEqual(self.post.comments.count(), 2)

    def test_add_comment_unauthenticated(self):
        """
        Test adding a comment as an unauthenticated user
        """
        self.client.post(
            reverse('blog:add_comment', kwargs={'post_id': self.post.id}),
            {'content': 'New test comment'}
        )
        self.assertEqual(self.post.comments.count(), 1)  # Comment count unchanged

