# blog_project/blog/views/comment_views.py

from __future__ import annotations
from typing import TYPE_CHECKING
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Comment, Post
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.http.response import JsonResponse


if TYPE_CHECKING:
    from django.http.response import HttpResponseRedirect
    from django.core.handlers.wsgi import WSGIRequest
    from django.forms import ModelForm


class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    View to display and handle the form used for creating a new comment on a blog post.

    Attributes
    ----------
    model : Comment
        Model to create.
    template_name : str
        Path to the template form for creating the new comment.
    fields : List[str]
        List of fields to display in the comment creation form.
    """
    model = Comment
    template_name = 'blog/comments/comment_form.html'
    fields = ['content']

    def form_valid(self, form: ModelForm) -> HttpResponseRedirect:
        """
        Validates form.
        Assigns the current user as the comment author and links to the appropriate post.

        Parameters
        ----------
        form : ModelForm
            The form instance for creating a comment.

        Returns
        -------
        HttpResponseRedirect
            The response to be sent to the client.
        """
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(slug=self.kwargs['slug'])
        return super().form_valid(form)


def comment_count(request: WSGIRequest, post_id: int):
    """
    Gets the number of comments on a post

    Parameters
    ----------
    request : WSGIRequest
    post_id : int
    """
    post = Post.objects.get(id=post_id)
    count = Comment.objects.filter(post=post).count()
    return JsonResponse({'comment_count': count})


@login_required
def add_comment(request: WSGIRequest, post_id: int):
    """
    Adds a comment to a blog post

    Parameters
    ----------
    request : WSGIRequest
    post_id : int
        The id of the blog post

    """
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        Comment.objects.create(
            post=post,
            author=request.user,
            content=request.POST['content']
        )
        messages.success(request, 'Your comment has been added.')
        return redirect('blog:post_detail', slug=post.slug)


@login_required
def delete_comment(request: WSGIRequest, comment_id: int):
    """
    Deletes a comment from a blog post

    Parameters
    ----------
    request : WSGIRequest
    comment_id : int
    """
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author or request.user.is_staff:
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
        return redirect('blog:post_detail', slug=comment.post.slug)
    else:
        messages.error(request, 'You do not have permission to delete this comment.')
    return redirect('blog:post_detail', slug=comment.post.slug)
