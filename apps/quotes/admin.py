from django.contrib import admin
from apps.quotes.models import Quote

class QuoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_created', 'active',)
    list_editable = ('active',)

admin.site.register(Quote, QuoteAdmin)
