from django.urls import path
from app.views import Index         

urlpatterns = [
    path("", Index.as_view()),
]