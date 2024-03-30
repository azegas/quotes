"""A module to register author app models to django admin."""

from django.db import models


class Author(models.Model):
    """Author model."""

    name = models.CharField(max_length=50, blank=False)
    lastname = models.CharField(max_length=50, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)
