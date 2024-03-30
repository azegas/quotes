"""File that contains the tests for Django models/orm."""

from datetime import datetime
from django.test import TestCase
from django.db.utils import IntegrityError
from apps.quotes.models import Quote
from apps.authors.models import Author


class TestQuoteModel(TestCase):
    """
    Class for tests.
    """

    def setUp(self):
        """
        Setup is so I don’t have to repeat Movie.objects.create(...) inside every test
        """
        self.author = Author.objects.create(name="Autorius")
        self.quote = Quote.objects.create(text="Test Quote", author=self.author, id=1)

    def test_unique_api_id_is_enforced(self):
        """
        Test that creation of two quotes with same id is not allowed

        Passes - IF the IntegrityError raises an error
        """

        with self.assertRaises(IntegrityError):
            Quote.objects.create(text="Another Test Quote", author=self.author, id=1)

    def test_added_date_automatically(self):
        """
        Test that the date is automatically saved on creation

        assert that quote.date_created is of the datetime type
        """

        self.assertTrue(type(self.quote.date_created), datetime)

    def test_active_false_by_default(self):
        """
        Test that boolean is set to false by default
        """
        self.assertTrue(
            isinstance(self.quote.active, bool)
        )  # ininstance is similar to "type()"
        self.assertFalse(self.quote.active)

    def test_str(self):
        """
        Test the __str__ method
        """
        expected = "Test Quote"
        actual = str(self.quote)

        self.assertEqual(expected, actual)
