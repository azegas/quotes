"""A module for quotes page forms. They are later used in the views.py"""

from django import forms
from apps.authors.models import Author


class QuoteForm(forms.Form):
    """
    ModelForm example:

    class QuoteForm(forms.ModelForm):
        class Meta:
            model = Quote
            fields = ["text", "author", "active"]
    """

    text = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4, "cols": 40}), max_length=200
    )  # if it was a modelForm, Django automatically render it as a textarea
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    active = forms.BooleanField(required=False)
