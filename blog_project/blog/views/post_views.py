# blog_project/blog/views/post_views.py

from __future__ import annotations
from typing import TYPE_CHECKING
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from ..models import Post
from ..forms import PostForm
from django.shortcuts import render, get_object_or_404

if TYPE_CHECKING:
    from django.http.response import HttpResponse, HttpResponseRedirect
    from django.core.handlers.wsgi import WSGIRequest
    from django.db.models.query import QuerySet
    from django.forms import ModelForm


class PostListView(ListView):
    """
    View to list all published posts.

    Attributes
    ----------
    model : Post
        Model to query.
    template_name : str
        Path to the template that renders the list of posts.
    context_object_name : str
        Name for the variable referenced in the template.
    paginate_by : int
        Number of posts to display per page.
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self) -> QuerySet:
        """
        Gets the published posts in order by creation_on date.

        Returns
        -------
        QuerySet
        """

        return Post.objects.filter(status='published').order_by('-created_on')


class PostDetailView(DetailView):
    """
    View to display the details of a single post.

    Attributes
    ----------
    model : Post
        Model to query.
    template_name : str
        Path to the template that renders the post details.
    """
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    View to the form that is used for creating a new blog post.

    Attributes
    ----------
    model : Post
        Model to create.
    template_name : str
        Path to the template form for creating the new post.
    fields : List[str]
        List of fields to display in the post creation form.
    """
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'image', 'status']

    def form_valid(self, form: ModelForm) -> HttpResponseRedirect:
        """
        Validates form.
        Assigns the current user as the post author before form validation.

        Parameters
        ----------
        form : ModelForm
            The form instance for creating a post.

        Returns
        -------
        HttpResponseRedirect
            The response to be sent to the client.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for updating an existing blog post.

    Attributes
    ----------
    model : Post
        Model to update.
    template_name : str
        Path to the template form used for updating a post.
    fields : List[str]
        List of fields to display in the post creation form.
    """
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'image', 'status']

    def test_func(self) -> bool:
        """
        Determines if the current user is allowed to update the post.

        Returns
        -------
        bool
        """
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View to delete an existing post.

    Attributes
    ----------
    model : Post
        Model to delete.
    template_name : str
        Path to the template used for confirming deletion.
    success_url : str
        URL to redirect upon a successful deletion of a post.
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self) -> bool:
        """
        Check for validity in deletion.
        This Ensures the author is the one deleting.

        Returns
        -------
        bool
        """
        post = self.get_object()
        return self.request.user == post.author


# Add this test view
@login_required
def test_auth(request: WSGIRequest) -> HttpResponse:
    """
    Test View to display user authentication details.

    Parameters
    ----------
    request : WSGIRequest

    Returns
    -------
    HttpResponse
    """
    return render(request, 'blog/test_auth.html', {
        'user': request.user,
        'session': request.session.items(),
    })
