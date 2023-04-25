"""
To do Django testing of Views created for worldnews project to
view the posts.
"""

from django.test import TestCase, RequestFactory
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.models import User
from .models import Category, Post, Comment
from .forms import CommentForm
from .views import (PostCategory, PostList, PostDetail, PostLike,
                    PostDelete, CommentApproval, UserProfile, UserAdmin)


class TestPostCategory(TestCase):
    """
    This is a class to test view for post category.
    """
    def test_get(self):
        """
        To test if the posts of same category are on the home page.
        """
        category = Category.objects.create(title='test', category='test')
        test_response = self.client.get('/category/')
        self.assertEqual('news/index.html' in test_response.context, False)


class TestPostList(TestCase):
    """
    This is a class to test view for post list on the home page.
    """
    def setUp(self):
        """
        Setup for testing.
        """
        self.user = User.objects.create_user(
            username='test user',
            email='test@email.com',
            password='testpass',
        )
        self.user.save()

    def test_post_list(self):
        """
        To test if the post list is on the home page.
        """
        test_response = self.client.get('/posts/')
        self.assertEqual(test_response.status_code, 404, 'created on')
        self.assertFalse('news/index.html' in test_response.context)


class TestPostDetail(TestCase):
    """
    This is a class to test view for post detail on post detail page.
    """
    def setUp(self):
        """
        Setup for testing.
        """
        self.user = User.objects.create_user(
            username='test user',
            email='test@email.com',
            password='testpass',
        )
        self.user.save()

    def test_get(self):
        """
        To test if the posts detail is on the post detail page
        and allows the user to like the post after sign in.
        """
        queryset = Post.objects.filter(status=1)
        test_response = self.client.get(f'/posts/{queryset}')
        self.assertEqual(test_response.status_code, 404)
        self.assertFalse('news/post_detail.html' in test_response.context)

    def test_post(self):
        """
        To test if the posts detail is on the post detail page
        and allows the user to like and comment on a post after sign in.
        """
        queryset = Post.objects.filter(status=1)
        test_response = self.client.post(f'/posts/{queryset}')
        self.assertEqual(test_response.status_code, 404)
        self.assertFalse('news/post_detail.html' in test_response.context)


class TestPostLike(TestCase):
    """
    This is a class to test view for number of likes on the post.
    """
    def setUp(self):
        """
        Setup for testing.
        """
        self.user = User.objects.create_user(
            username='test user',
            email='test@email.com',
            password='testpass',
        )
        self.user.save()

    def test_post(self):
        """
        To test if the count of number of likes on the post is
        on post detail page.
        """
        test_response = self.client.get('/posts/')
        post = Post.objects.create(title='Test post')
        post.likes.add(self.user)
        self.assertEqual(test_response.status_code, 404)
        self.assertEqual(post.likes.first(), self.user)
        self.assertFalse('news/post_detail.html' in test_response.context)


class TestPostDelete(TestCase):
    """
    This is a class to test view for post delete option on the home page.
    """
    def setUp(self):
        """
        Setup for testing.
        """
        self.user = User.objects.create_user(
            username='test user',
            email='test@email.com',
            password='testpass',
        )
        self.user.save()

    def test_can_delete_post(self):
        """
        To test if the post delete option is on the home page for
        post authors to delete their own posts and superuser to
        delete all the posts.
        """
        post = Post.objects.create(title='Test post')
        test_response = self.client.get('/posts/')
        self.assertEqual(test_response.status_code, 404)
        self.assertEqual(post.delete(), (1, {'news.Post': 1}))
        self.assertFalse('news/index.html' in test_response.context)


class TestCommentApproval(TestCase):
    """
    This is a class to test view for comments need or do not need
    approval message for the admin.
    """
    def test_get(self):
        """
        To test if there is a message for the admin if comments need or
        do not need approval on each post.
        """
        test_response = self.client.get('/posts/')
        post = Post.objects.create(title='Test post')
        self.assertEqual(test_response.status_code, 404)
        self.assertTrue(test_response, 'news/non_approve_comment.html')
        self.assertTrue(test_response, 'news/approve_comment.html')


class TestUserProfile(TestCase):
    """
    This is a class to test view for user profile on profile page.
    """
    def test_get(self):
        """
        To test if the profile of user is on profile page after sign in.
        """
        test_response = self.client.get('/users/')
        user = User.objects.create_user(username='Test user')
        self.assertEqual(test_response.status_code, 404)
        self.assertTrue(test_response, 'news/profile.html')


class TestUserAdmin(TestCase):
    """
    This is a class to test view for the admin to access admin panel with
    the link to the admin provided on the admin page and navigation bar
    of Admin on the home page
    """
    def test_get(self):
        """
        To test if the admin has access to admin panel after sign in.
        """
        test_response = self.client.get('/users/')
        user = User.objects.create_user(username='Test user')
        self.assertEqual(test_response.status_code, 404)
        self.assertTrue(test_response, 'news/admin.html')
