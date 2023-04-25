"""
To do Django testing of a form created for the
site owner/site users to comment on a post.
"""

from django.test import TestCase
from .forms import CommentForm


class TestCommentForm(TestCase):
    """
    This is a class to test a form created to comment on a post.
    """
    def test_comment_comment_is_required(self):
        """
        To print a message that this field is required if there is not
        a comment in a comment form.
        """
        form = CommentForm({'comment': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('comment', form.errors.keys())
        self.assertEqual(form.errors['comment'][0], 'This field is required.')

    def test_fields_are_explicit_in_form_metaclass(self):
        """
        To print a comment if there is a comment in a comment form.
        """
        form = CommentForm()
        self.assertEqual(form.Meta.fields, ['comment'])
