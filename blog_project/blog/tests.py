from datetime import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment
from django.core.files.uploadedfile import SimpleUploadedFile
from .models.Post import Status


POST_TITLE = 'Test Post'
POST_CONTENT = 'Test content'
COMMENT_CONTENT = 'Test comment'


class BlogTests(TestCase):
    """
    Tests for post and comment creation / editing

    To run -> python manage.py test
    """
    def setUp(self):
        # CREATE USERS
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@test.com'
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


