"""
App configuration for the Authors application.

This module contains the Django configuration for the 'authors' app. It defines
app-specific settings, such as the application's name and the default auto field
type for model primary keys. The use of 'BigAutoField' as the default auto field
implies expecting a large number of objects, suitable for applications with
significant database records.

The 'AuthorsConfig' class within this module is used by Django's app registry
to configure app-specific settings.

See Django's documentation on applications and AppConfig for more information:
https://docs.djangoproject.com/en/stable/ref/applications/
"""

from django.apps import AppConfig


class AuthorsConfig(AppConfig):
    """
    Configuration for the 'authors' application.

    Overrides the default auto field type with 'BigAutoField' to accommodate
    tables with a large number of entries. It also sets the application's
    name within the Django project.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.authors"
