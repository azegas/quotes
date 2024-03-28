from django.contrib import admin
from apps.authors.models import Author

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'lastname',)
    list_editable = ('name',)

admin.site.register(Author, AuthorAdmin)
