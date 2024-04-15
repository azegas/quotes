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
        self.author = Author.objects.create(name="Test Author")

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

    def test_author_detail_view(self):
        """test author detail view"""

        url = reverse("author-detail", kwargs={"pk": self.author.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "authors/author_detail.html")
        self.assertIn("object", response.context)
        self.assertContains(response, "Test Author")

    def test_author_create_view(self):
        """test author create view"""

        form_data = {
            "name": "sukurtas",
            "lastname": "testo",
        }

        url = reverse("author-create")
        response = self.client.post(url, data=form_data)
        self.assertRedirects(response, reverse("author-list"))
        created_author = Author.objects.get(name="sukurtas")
        self.assertEqual(created_author.name, "sukurtas")
        self.assertEqual(created_author.lastname, "testo")

    def test_author_delete_view(self):
        """test author delete view"""

        url = reverse("author-delete", kwargs={"pk": self.author.pk})
        initial_count = Author.objects.count()
        response = self.client.post(url)
        self.assertRedirects(response, reverse("author-list"))
        self.assertEqual(Author.objects.count(), initial_count - 1)
        self.assertFalse(Author.objects.filter(pk=self.author.pk).exists())

    def test_author_update_view(self):
        """test author update view"""

        form_data = {
            "name": "after",
            "lastname": "test",
        }

        url = reverse("author-update", kwargs={"pk": self.author.pk})
        response = self.client.post(url, data=form_data)
        self.assertRedirects(response, reverse("author-list"))
        # Refresh the author instance from the database to get the updated data
        self.author.refresh_from_db()
        self.assertEqual(self.author.name, form_data["name"])
        self.assertEqual(self.author.lastname, form_data["lastname"])
