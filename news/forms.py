"""
Create a form for the site owner/site users
to comment on a post.
"""

from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """
    This is a class to create a form to comment on a post.
    """
    class Meta:
        model = Comment
        fields = ['comment', ]
