"""File that contains the tests for Django views"""

from django.test import Client, TestCase
from django.urls import reverse

from apps.authors.models import Author


class TestViews(TestCase):
    """
    Class for tests.
    """

    def setUp(self):
        """
        setUp method is simply for creating all kinds of objects that we will
        use/reuse in the tests below, later.
        """

        self.client = Client()
        self.index_url = reverse("index")
        # Create some test authors
        Author.objects.create(name="Test Author 1")
        Author.objects.create(name="Test Author 2")

    def test_index_get(self):
        """test index view"""
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "project/index.html")

    def test_author_list_view(self):
        """test author list view"""

        url = reverse("author-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "authors/author_list.html")
        self.assertIn("author_list", response.context)
        self.assertContains(response, "Test Author 1")
        self.assertContains(response, "Test Author 2")
