"""
Create Models for worldnews project to manage the posts.
Create Category model to categorize the posts.
Create Post model to draft a post.
Creat Comment model to comment on a post.
"""

from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


STATUS = ((0, "Draft"), (1, "Published"))


class Category(models.Model):
    """
    This is a class to create Category model to categorize the posts.
    """
    category = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=100, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        To return the title of the category.
        """
        return self.category


class Post(models.Model):
    """
    This is a class to create Post model to draft a post.
    """
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name="news_posts")
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='news_likes', blank=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        """
        To return the title of the post.
        """
        return self.title

    def number_of_likes(self):
        """
        To return number of likes on the post.
        """
        return self.likes.count()


class Comment(models.Model):
    """
    This is a class to create Comment model to comment on a post.
    """
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        """
        To return the name and comment of users.
        """
        return f"Comment {self.comment} by {self.name}"
