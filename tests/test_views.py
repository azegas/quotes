"""File that contains the tests for Django views"""

from django.test import Client, TestCase
from django.urls import reverse

from apps.authors.models import Author
from apps.quotes.forms import QuoteForm
from apps.quotes.models import Quote

# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods


class TestViews(TestCase):
    """Class for view tests"""

    def setUp(self):
        """
        setUp method is simply for creating all kinds of objects that we will
        use/reuse in the tests below, later.
        """

        self.client = Client()
        self.index_url = reverse("index")
        self.author_list_url = reverse("author-list")
        self.quote_list_url = reverse("quote-list")
        self.author1 = Author.objects.create(name="Test Author 1")
        self.author2 = Author.objects.create(name="Test Author 2")
        self.quote1 = Quote.objects.create(text="Test Quote 1")
        self.quote2 = Quote.objects.create(text="Test Quote 2")

    def test_index_get(self):
        """test index view"""

        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "project/index.html")

    def test_author_list_view(self):
        """test author list view"""

        url = self.author_list_url
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "authors/author_list.html")
        self.assertIn("author_list", response.context)
        self.assertContains(response, self.author1)
        self.assertContains(response, self.author1)

    def test_author_detail_view(self):
        """test author detail view"""

        url = reverse("author-detail", kwargs={"pk": self.author1.pk})
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
        created_author = Author.objects.get(name=form_data["name"])

        self.assertRedirects(response, self.author_list_url)
        self.assertEqual(created_author.name, form_data["name"])
        self.assertEqual(created_author.lastname, form_data["lastname"])

    def test_author_delete_view(self):
        """test author delete view"""

        url = reverse("author-delete", kwargs={"pk": self.author1.pk})
        initial_count = Author.objects.count()
        response = self.client.post(url)

        self.assertRedirects(response, self.author_list_url)
        self.assertEqual(Author.objects.count(), initial_count - 1)
        self.assertFalse(Author.objects.filter(pk=self.author1.pk).exists())

    def test_author_update_view(self):
        """test author update view"""

        form_data = {
            "name": "after",
            "lastname": "test",
        }

        url = reverse("author-update", kwargs={"pk": self.author1.pk})
        response = self.client.post(url, data=form_data)

        self.assertRedirects(response, self.author_list_url)
        # Refresh the author instance from the database to get the updated data
        self.author1.refresh_from_db()
        self.assertEqual(self.author1.name, form_data["name"])
        self.assertEqual(self.author1.lastname, form_data["lastname"])

    def test_quote_list_view(self):
        """test quote list view"""

        response = self.client.get(self.quote_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quotes/quote_list.html")
        self.assertIn("object_list", response.context)
        self.assertContains(response, self.quote1.text)
        self.assertContains(response, self.quote2.text)

    def test_quote_list_view_with_query(self):
        """test quote list view when there is a query passed in"""

        # query is 1, we should find a "Test Quote 1" in the response
        query = "1"
        url = reverse("quote-list") + f"?q={query}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quotes/quote_list.html")
        self.assertContains(response, self.quote1.text)

    def test_quote_detail_view(self):
        """test quote detail view"""

        url = reverse("quote-detail", kwargs={"pk": self.quote1.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quotes/quote_detail.html")
        self.assertContains(response, self.quote1.text)

    def test_quote_create_view_get(self):
        """Test GET request to quote create view"""

        url = reverse("quote-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quotes/quote_form.html")
        self.assertTrue("form" in response.context)
        self.assertIsInstance(response.context["form"], QuoteForm)

    def test_quote_create_view_post(self):
        """test POST request to quote create view"""

        form_data = {
            "text": "labadiena",
            "author": self.author1.pk,
        }

        url = reverse("quote-create")
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 302)  # status code for redirect
        self.assertRedirects(response, self.quote_list_url)
        self.assertTrue(
            Quote.objects.filter(
                text=form_data["text"], author=self.author1
            ).exists()
        )

    def test_quote_create_view_post_invalid_form(self):
        """Test POST request with invalid form data"""

        form_data = {
            "text": "",  # Invalid: Text is required
            "author": self.author1.pk,
        }
        url = reverse("quote-create")
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quotes/quote_form.html")
        self.assertTrue("form" in response.context)
        self.assertIsInstance(response.context["form"], QuoteForm)
        form = response.context["form"]
        self.assertTrue(form.errors)

    def test_quote_delete_view_get(self):
        """test quote delete view, GET request"""

        url = reverse("quote-delete", kwargs={"pk": self.quote1.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quotes/quote_confirm_delete.html")

    def test_quote_delete_view_post(self):
        """test quote delete view, POST request"""

        initial_count = Quote.objects.count()
        url = reverse("quote-delete", kwargs={"pk": self.quote1.pk})
        response = self.client.post(url)

        self.assertFalse(Quote.objects.filter(pk=self.quote1.pk).exists())
        self.assertRedirects(response, self.quote_list_url)
        self.assertEqual(Quote.objects.count(), initial_count - 1)

    def test_quote_update_view(self):
        """test quote update view"""

        url = reverse("quote-update", kwargs={"pk": self.quote1.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quotes/quote_form.html")
        self.assertTrue("form" in response.context)
        form = response.context["form"]
        self.assertIsInstance(form, QuoteForm)
        self.assertEqual(form["text"].value(), self.quote1.text)

    def test_quote_update_view_get(self):
        """test quote update view, GET request"""

        url = reverse("quote-update", kwargs={"pk": self.quote1.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quotes/quote_form.html")
        self.assertTrue("form" in response.context)
        self.assertIsInstance(response.context["form"], QuoteForm)

    def test_quote_update_view_post(self):
        """test quote update view, POST request"""

        form_data = {
            "text": "Updated text",
            "author": self.author1.pk,
        }

        url = reverse("quote-update", kwargs={"pk": self.quote1.pk})
        response = self.client.post(url, data=form_data)
        updated_quote = Quote.objects.get(pk=self.quote1.pk)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.quote_list_url)
        self.assertEqual(updated_quote.text, form_data["text"])
        self.assertEqual(updated_quote.author.pk, form_data["author"])

    def test_quote_update_view_post_invalid(self):
        """Test quote update view with invalid form data, POST request"""

        form_data = {
            "text": "",  # Empty text field
            "author": self.author1.pk,
        }

        url = reverse("quote-update", kwargs={"pk": self.quote1.pk})
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quotes/quote_form.html")
        self.assertTrue("form" in response.context)
        form = response.context["form"]
        self.assertIsInstance(form, QuoteForm)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.errors)

        # Optionally, you can check specific error messages if needed
        self.assertTrue("text" in form.errors)
        self.assertEqual(form.errors["text"], ["This field is required."])

        self.assertNotEqual(
            Quote.objects.get(pk=self.quote1.pk).text, form_data["text"]
        )
        self.assertEqual(
            Quote.objects.get(pk=self.quote1.pk).text, "Test Quote 1"
        )

    def test_project_show_random_quote_generator_true(self):
        """Test project index view if it returns the correct boolean value"""

        # # Create three quotes in the database
        Quote.objects.create(text="Quote 1")
        Quote.objects.create(text="Quote 2")
        Quote.objects.create(text="Quote 3")

        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["show_random_quote_generator"])

    def test_project_show_random_quote_generator_false(self):
        """Test project index view if it returns the correct boolean value"""

        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["show_random_quote_generator"])

    def test_project_random_quote_view_get(self):
        """test project RandomQuote view, GET request"""

        url = reverse("random-quote")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project/partials/random_quote.html")
        self.assertIn("random_quote", response.context)

    def test_project_random_quote_view_get_no_quotes(self):
        """test project RandomQuote view, GET request, when no quotes exist"""

        # Delete all quotes from the database
        Quote.objects.all().delete()

        url = reverse("random-quote")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project/partials/no_quotes.html")
