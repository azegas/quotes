"""File that contains the tests for Django models/orm."""

from datetime import datetime

from django.db.utils import IntegrityError
from django.test import TestCase

from apps.authors.models import Author
from apps.quotes.models import Quote


class TestModels(TestCase):
    """Class for model tests"""

    def setUp(self):
        """Setup is so I don’t have to repeat Movie.objects.create(...)"""

        self.author = Author.objects.create(
            id=1,
            name="Autorius",
            lastname="Petravicius",
        )
        self.quote = Quote.objects.create(
            id=1,
            text="Test Quote",
            author=self.author,
        )

    def test_quote_is_created(self):
        """Test that creation of the quotes works"""
        self.assertTrue(
            Quote.objects.filter(
                id=1,
                text="Test Quote",
                author=self.author,
            ).exists()
        )

    def test_author_is_created(self):
        """Test that creation of authors works"""
        self.assertTrue(
            Author.objects.filter(
                id=1,
                name="Autorius",
                lastname="Petravicius",
            ).exists()
        )

    def test_quote_unique_id_is_enforced(self):
        """Test that creation of two quotes with same id is not allowed.
        Passes - IF the IntegrityError raises an error"""

        with self.assertRaises(IntegrityError):
            Quote.objects.create(
                id=1,
                text="Another Test Quote",
                author=self.author,
            )

    def test_author_unique_id_is_enforced(self):
        """Test that creation of two authors with same id is not allowed.
        Passes - IF the IntegrityError raises an error"""

        with self.assertRaises(IntegrityError):
            Quote.objects.create(
                id=1,
                text="Another Test Quote",
                author=self.author,
            )

    def test_quote_added_date_automatically(self):
        """Test that the date is automatically saved on creation assert that
        quote.date_created is of the datetime type"""

        self.assertTrue(type(self.quote.date_created), datetime)

    def test_author_added_date_automatically(self):
        """Test that the date is automatically saved on creation assert that
        author.date_created is of the datetime type"""

        self.assertTrue(type(self.author.date_created), datetime)

    def test_quote_active_false_by_default(self):
        """Test that boolean is set to false by default"""

        self.assertTrue(
            isinstance(self.quote.active, bool)
        )  # ininstance is similar to "type()"
        self.assertFalse(self.quote.active)

    def test_str_quote(self):
        """Test the __str__ method of quote model"""

        expected = "Test Quote"
        actual = str(self.quote)

        self.assertEqual(expected, actual)

    def test_str_author(self):
        """test the __str__ method of author model"""

        expected = "Autorius"
        actual = str(self.author)

        self.assertEqual(expected, actual)
