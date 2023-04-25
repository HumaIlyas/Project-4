"""
App news for the worldnews project.
"""

from django.apps import AppConfig


class NewsConfig(AppConfig):
    """
    This is a class to configure news from news app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
