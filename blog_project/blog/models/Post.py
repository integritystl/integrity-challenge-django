# blog_project/blog/models/Post.py
from typing import List, Tuple
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from . import AbstractPost


class Status:
    """
    Class for holding string vars used in describing post current status
    """
    draft = 'draft'
    Draft = 'Draft'
    published = 'published'
    Published = 'Published'

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        """
        Gets the database and prety value of the different status choices

        Returns
        -------
        List[Tuple[str, str]]
        """
        return [(cls.draft, cls.Draft), (cls.published, cls.Published)]

    @classmethod
    def default(cls) -> str:
        """
        Gets the default status

        Returns
        -------
        str
        """
        return cls.draft


class Post(AbstractPost):
    """
    Represents a blog post

    Attributes
    ----------
    title : CharField
        The title of the post. Limited to 200 characters.
    slug : SluField
        A unique identifier for the post. Limited to 200 characters.
        If not provided, It will be generated based on the title.
    author : ForeignKey
        Person that wrote the post. Linked to a User model.
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
    image = models.ImageField(upload_to='posts/%Y/%m/%d/', blank=True)
    status = models.CharField(max_length=10, choices=Status.choices(), default=Status.default())

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
