# blog_project/blog/models/Comment.py

from django.db import models
from . import AbstractPost, Post


class Comment(AbstractPost):
    """
    Represents a blog post Comment

    Attributes
    ----------
    author : ForeignKey
        Person that wrote the post. Linked to a User model.
    content : models.TextField
        What is written in the post.
    created_on : DateTimeField
        The date and time the post was created. Automatically created on save.
    updated_on : DatTimeField
        The date and time the post was last updated. Automatically created upon save.
    post :
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'Comment by {self.author} on {self.post.title} at {self.created_on}'
