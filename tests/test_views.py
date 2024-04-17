"""File that contains the tests for Django views"""

from django.test import Client, TestCase
from django.urls import reverse

from apps.authors.models import Author
from apps.quotes.forms import QuoteForm
from apps.quotes.models import Quote


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

        # Create some test data later used in the tests
        Author.objects.create(name="Test Author 1")
        Author.objects.create(name="Test Author 2")
        self.author = Author.objects.create(name="Test Author")
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
        created_author = Author.objects.get(name=form_data["name"])
        self.assertEqual(created_author.name, form_data["name"])
        self.assertEqual(created_author.lastname, form_data["lastname"])

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

    def test_quote_list_view(self):
        """test quote list view"""

        # Make a GET request to the view using the test client
        response = self.client.get(reverse("quote-list"))

        # Check that the response is rendered using the correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quotes/quote_list.html")

        # Check that the quotes are included in the response context
        self.assertIn("object_list", response.context)
        self.assertContains(response, self.quote1.text)
        self.assertContains(response, self.quote2.text)

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

        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, "quotes/quote_form.html")

        # Check that the form is passed to the template context
        self.assertTrue("form" in response.context)
        self.assertIsInstance(response.context["form"], QuoteForm)

    def test_quote_create_view_post(self):
        """test POST request to quote create view"""

        form_data = {
            "text": "labadiena",
            "author": self.author.pk,
        }

        url = reverse("quote-create")
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 302)  # status code for redirect
        self.assertRedirects(response, reverse("quote-list"))
        # Check that the newly created quote exists in the database
        self.assertTrue(
            Quote.objects.filter(
                text=form_data["text"], author=self.author
            ).exists()
        )

    def test_quote_create_view_post_invalid_form(self):
        """Test POST request with invalid form data"""

        # Create a POST request with invalid form data
        form_data = {
            "text": "",  # Invalid: Text is required
            "author": self.author.pk,
        }
        url = reverse("quote-create")
        response = self.client.post(url, data=form_data)

        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, "quotes/quote_form.html")

        # Check that the form is passed to the template context
        self.assertTrue("form" in response.context)
        self.assertIsInstance(response.context["form"], QuoteForm)

        # Check that the form contains errors
        form = response.context["form"]
        self.assertTrue(form.errors)

    def test_quote_delete_view_get(self):
        """test quote delete view, GET request"""

        url = reverse("quote-delete", kwargs={"pk": self.quote1.pk})
        response = self.client.get(url)

        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, "quotes/quote_confirm_delete.html")

    def test_quote_delete_view_post(self):
        """test quote delete view, POST request"""

        # Get the initial count of quotes
        initial_count = Quote.objects.count()

        # Get the URL for deleting the quote
        url = reverse("quote-delete", kwargs={"pk": self.quote1.pk})

        # Make a POST request to delete the quote
        response = self.client.post(url)

        # Check that the quote has been deleted
        self.assertFalse(Quote.objects.filter(pk=self.quote1.pk).exists())

        # Optionally, check the redirect after deletion
        self.assertRedirects(response, reverse("quote-list"))

        # Check that the count of quotes has decreased by 1
        self.assertEqual(Quote.objects.count(), initial_count - 1)

    def test_quote_update_view(self):
        """test quote update view"""

        url = reverse("quote-update", kwargs={"pk": self.quote1.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quotes/quote_form.html")

        # Check that the form is passed to the template context
        self.assertTrue("form" in response.context)
        form = response.context["form"]
        self.assertIsInstance(form, QuoteForm)

        # Check the initial form data
        self.assertEqual(form["text"].value(), self.quote1.text)

    def test_quote_update_view_get(self):
        """test quote update view, GET request"""

        # Get the URL for updating the quote
        url = reverse("quote-update", kwargs={"pk": self.quote1.pk})

        # Make a GET request to retrieve the update form
        response = self.client.get(url)

        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, "quotes/quote_form.html")

        # Check that the form is passed to the template context
        self.assertTrue("form" in response.context)
        self.assertIsInstance(response.context["form"], QuoteForm)

    def test_quote_update_view_post(self):
        """test quote update view, POST request"""

        # Define the form data for updating the quote
        form_data = {
            "text": "Updated text",
            "author": self.author.pk,
        }

        # Get the URL for updating the quote
        url = reverse("quote-update", kwargs={"pk": self.quote1.pk})

        # Make a POST request to update the quote
        response = self.client.post(url, data=form_data)

        # Check that the response is a redirect to the quote list
        self.assertEqual(response.status_code, 302)  # status code for redirect
        self.assertRedirects(response, reverse("quote-list"))

        # Check that the quote has been updated in the database
        updated_quote = Quote.objects.get(pk=self.quote1.pk)
        self.assertEqual(updated_quote.text, form_data["text"])
        self.assertEqual(updated_quote.author.pk, form_data["author"])

    def test_quote_update_view_post_invalid(self):
        """Test quote update view with invalid form data, POST request"""

        # Define invalid form data with empty text field
        form_data = {
            "text": "",  # Empty text field
            "author": self.author.pk,
        }

        # Get the URL for updating the quote
        url = reverse("quote-update", kwargs={"pk": self.quote1.pk})

        # Make a POST request with invalid form data
        response = self.client.post(url, data=form_data)

        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, "quotes/quote_form.html")

        # Check that the form is passed to the template context
        self.assertTrue("form" in response.context)
        form = response.context["form"]
        self.assertIsInstance(form, QuoteForm)

        # Check that the form is bound and contains errors
        self.assertTrue(form.is_bound)
        self.assertTrue(form.errors)

        # Optionally, you can check specific error messages if needed
        self.assertTrue("text" in form.errors)
        self.assertEqual(form.errors["text"], ["This field is required."])

        # Verify that the quote object is not updated in the database
        self.assertNotEqual(
            Quote.objects.get(pk=self.quote1.pk).text, form_data["text"]
        )

        # Verify that the quote object is same as at the beginning
        self.assertEqual(
            Quote.objects.get(pk=self.quote1.pk).text, "Test Quote 1"
        )
