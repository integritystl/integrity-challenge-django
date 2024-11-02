# blog_project/blog/models/AbstractPost.py

from django.db import models
from django.contrib.auth.models import User


class AbstractPost(models.Model):
    """
    Abstract class for Models that represent user generated content

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

    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_related')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Attributes
        ----------
        ordering : List[str]
            Orders the posts by created_on attribute.
        indexes : List[Index]
            Creates an index based on the created_on attribute.
        """
        abstract = True
        ordering = ['-created_on']
        indexes = [
            models.Index(fields=['-created_on']),
        ]
