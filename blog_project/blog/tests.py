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
USER_DATA = {'username': USERNAME, 'password': PASSWORD}

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
        self.user = User.objects.create_user(**USER_DATA)
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
        self.client.login(**USER_DATA)
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

    def test_delete_comment_authorized(self):
        """
        Test deleting a comment as the comment author
        """
        self.client.login(**USER_DATA)
        self.client.post(
            reverse('blog:delete_comment', kwargs={'comment_id': self.comment.id})
        )
        self.assertEqual(self.post.comments.count(), 0)

    def test_delete_comment_unauthorized(self):
        """Test deleting a comment as another user"""
        # Create another user
        other_username, other_password = 'other', 'other123'
        User.objects.create_user(
            username=other_username,
            password=other_password
        )
        self.client.login(username=other_username, password=other_password)
        response = self.client.post(
            reverse('blog:delete_comment', kwargs={'comment_id': self.comment.id})
        )
        self.assertEqual(self.post.comments.count(), 1)

    def test_comment_ordering(self):
        """
        Test that comments are ordered correctly
        """
        new_comment = 'New comment'
        Comment.objects.create(
            post=self.post,
            author=self.user,
            content=new_comment
        )
        comments = self.post.comments.all()
        self.assertEqual(comments[0].content, new_comment)  # Newest first
        self.assertEqual(comments[1].content, COMMENT_CONTENT)

    def test_post_delete(self):
        """
        Test deleting a post
        """
        self.client.login(**USER_DATA)
        response = self.client.post(
            reverse('blog:post_delete', kwargs={'slug': self.post.slug})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(Comment.objects.count(), 0)
