# blog/models.py

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Post(models.Model):
    """
    Represents a blog post

    Attributes
    ----------
    title : CharField
        The title of the blog post. Limited to 200 characters.
    slug : SluField
        A unique identifier for the post. Limited to 200 characters.
        If not provided, It will be generated based on the title.
    author : ForeignKey
        Person that wrote the blog post. Linked to a User model.
    content : models.TextField
        What is written in the post.
    image : ImageField
        Optional image for the post
    created_on : DateTimeField
        The date and time the post was created. Automatically created on save.
    updated_on : DatTimeField
        The date and time the post was last updated. Automatically created upon save.
    status : CharField
        String representation of the current state of the post.
        Choices are either 'draft' or 'published'. Default is 'draft'
        Limited to 10 characters.

    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    image = models.ImageField(upload_to='posts/%Y/%m/%d/', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=[
        ('draft', 'Draft'),
        ('published', 'Published')
    ], default='draft')

    class Meta:
        """
        Attributes
        ----------
        ordering : List[str]
            Orders the posts by created_on attribute.
        indexes : List[Index]
            Creates an index based on the created_on attribute.
        """
        ordering = ['-created_on']
        indexes = [
            models.Index(fields=['-created_on']),
        ]

    def __str__(self) -> str:
        """
        Gets the title of the post

        Returns
        -------
        str
        """
        return self.title

    def save(self, *args, **kwargs):
        """
        Saves the post to the database. Generates a slug if needed.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        """
        Gets the url of the post

        Returns
        -------
        str
        """
        return reverse('blog:post_detail', args=[self.slug])
