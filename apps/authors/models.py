from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=50, blank=False)
    lastname = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name