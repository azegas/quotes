"""A module to register quotes app models to django admin."""

from django.contrib import admin
from apps.quotes.models import Quote


class QuoteAdmin(admin.ModelAdmin):
    """A modification to the default quote model admin."""

    list_display = (
        "id",
        "date_created",
        "active",
    )
    list_editable = ("active",)


admin.site.register(Quote, QuoteAdmin)
