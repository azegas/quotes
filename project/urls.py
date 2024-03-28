from django.contrib import admin
from django.urls import path, include
from project.views import Index, RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", Index.as_view(), name="index"),
    path("rdt", RedirectView.as_view(), name="rdt"),
    path('quotes/', include('apps.quotes.urls')),
    path('authors/', include('apps.authors.urls')),
]
