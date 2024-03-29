from django.db import models
from datetime import datetime
from apps.authors.models import Author

class Quote(models.Model):
    text = models.TextField(blank=False, null=False)
    author = models.ForeignKey(
        Author,
        null=True, # setting this so on_delete (below) works
        on_delete= models.SET_NULL, # on delete - set the value to NULL
    )
    active = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"quote id - {str(self.id)}, author - {str(self.author_id)}"