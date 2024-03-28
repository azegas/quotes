from django.db import models
from datetime import datetime


class Author(models.Model):
    name = models.CharField(max_length=50, blank=False)
    lastname = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Quote(models.Model):
    text = models.TextField(blank=False, null=False)
    author = models.ForeignKey(
        Author,
        null=True, # setting this so on_delete works
        on_delete= models.SET_NULL, # on delete - set the value to NULL
    )
    active = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=datetime.now(), editable=False)

    def __str__(self):
        return f"quote id - {str(self.id)}, author - {str(self.author_id)}"