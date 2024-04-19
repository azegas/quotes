"""File that contains the tests for Django forms"""

from django.test import TestCase

from apps.authors.models import Author
from apps.quotes.forms import QuoteForm


class TestForms(TestCase):
    """Class for form tests"""

    def setUp(self):
        """
        setUp method is simply for creating all kinds of objects that we will
        use/reuse in the tests below, later.
        """

        self.author1 = Author.objects.create(name="Test Author 1")

    def test_quote_form_valid_data(self):
        """Test that the form is valid with correct data"""

        form = QuoteForm(
            data={
                "text": "hello",
                "author": self.author1.pk,
                "active": True,
            }
        )

        self.assertTrue(form.is_valid())

    def test_quote_form_no_data(self):
        """Test that the form breaks if no data is submitted"""

        form = QuoteForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(
            len(form.errors), 2
        )  # one error per field? but why not 3? ;)
