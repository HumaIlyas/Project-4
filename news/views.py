"""
Create Views for worldnews project to view the posts based on Category,
Post, and Comment models for PostCategory, PostList, PostDetail,
PostLike, PostDelete, CommentApproval, UserProfile, and UserAdmin.
"""

from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Category, Post
from .forms import CommentForm


class PostCategory(View):
    """
    This is a class to create view for post category.
    """
    def get(self, request, *args, **kwargs):
        """
        To return the posts of same category on the home page.
        """
        queryset = list(Post.objects.filter(
            category__category=kwargs['category'].title()))
        context = {
            "post_list": queryset
        }
        return render(request, "news/index.html", context)


class PostList(generic.ListView):
    """
    This is a class to create view for post list on the home page.
    """
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "news/index.html"
    paginate_by = 6


class PostDetail(View):
    """
    This is a class to create view for post detail.
    """
    def get(self, request, slug, *args, **kwargs):
        """
        To return the posts detail on the post detail page
        and allows the user to like the post after sign in.
        """
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        context = {
            "post": post,
            "comments": comments,
            "commented": False,
            "liked": liked,
            "comment_form": CommentForm()
        }
        return render(request, "news/post_detail.html", context)

    def post(self, request, slug, *args, **kwargs):
        """
        To return the posts detail on the post detail page
        and allows the user to like and comment on a post after sign in.
        """
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        context = {
            "post": post,
            "comments": comments,
            "commented": True,
            "liked": liked,
            "comment_form": CommentForm()
        }
        return render(request, "news/post_detail.html", context)


class PostLike(View):
    """
    This is a class to create view for number of likes on the post.
    """
    def post(self, request, slug, *args, **kwargs):
        """
        To return the count of number of likes on the post on post detail page.
        """
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('news/post_detail', args=[slug]))


class PostDelete(View):
    """
    This is a class to create view for post delete option on the home page.
    """
    def get(self, request, slug, *args, **kwargs):
        """
        To return the post delete option for post authors to
        delete their own posts and superuser to delete all the posts.
        """
        post = get_object_or_404(Post, slug=slug)
        if request.user.is_superuser or request.user == post.author:
            post.delete()
        else:
            raise PermissionDenied

        return render(request, "news/index.html")


class CommentApproval(View):
    """
    This is a class to create view for comments need or do not need
    approval message for the admin.
    """
    def get(self, request, slug, *args, **kwargs):
        """
        To return message for the admin if comments need or
        do not need approval on each post.
        """
        post = get_object_or_404(Post, slug=slug)
        if post.comments.filter(approved=False).exists():
            if request.user.is_superuser:
                return render(request, "news/approve_comment.html")
        else:
            return render(request, 'news/non_approve_comment.html')


class UserProfile(View):
    """
    This is a class to create view for user profile on profile page.
    """
    def get(self, request):
        """
        To return profile of user after sign in.
        """
        if request.user.is_authenticated:
            return render(request, "news/profile.html")


class UserAdmin(View):
    """
    This is a class to create view for the admin to access admin panel with
    the link to the admin provided on the admin page and navigation bar
    of Admin on the home page.
    """
    def get(request):
        """
        To return admin panel for admin after sign in.
        """
        if request.user.is_superuser:
            return render(request, "news/admin.html")
