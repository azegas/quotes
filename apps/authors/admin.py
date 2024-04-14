"""A module to register authors app models to django admin."""

from django.contrib import admin

from apps.authors.models import Author


class AuthorAdmin(admin.ModelAdmin):
    """A modification to the default author model admin."""

    list_display = (
        "id",
        "name",
        "lastname",
    )
    list_editable = ("name",)


admin.site.register(Author, AuthorAdmin)
