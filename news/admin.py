"""
Create Admin panel for the admin of worldnews project to manage the posts.
Create admin for Category model to categorize the posts.
Create admin for Post model to draft a post.
Creat admin for Comment model to comment on a post as well as
approve/disapprove the offensive comments.
"""

from django.contrib import admin
from .models import Category, Post, Comment
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    This is a class to create admin for Category model to
    categorize the posts.
    """
    list_display = ('category', 'title', 'created_on')
    list_filter = ('category', 'created_on')
    search_fields = ('category', 'title')


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """
    This is a class to create admin for Post model to draft a post.
    """
    list_display = ('category', 'title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'category', 'created_on')
    summernote_fields = ('content')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    This is a class to create admin for Comment model to comment
    on a post as well as approve/disapprove the offensive comments.
    """
    list_display = ('name', 'comment', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'comment')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
