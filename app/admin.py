from django.contrib import admin
from app.models import Quote, Author

# Register your models here.

class QuoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_created', 'active',)
    list_editable = ('active',)

admin.site.register(Author)
admin.site.register(Quote, QuoteAdmin)
