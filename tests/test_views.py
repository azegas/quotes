"""File that contains the tests for Django views"""

from django.contrib.auth.models import User
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
        self.user = User.objects.create_user(
            username="test",
            email="testuser@gmail.com",
            password="password",
            is_superuser=True,
            is_staff=True,
        )
        self.author_form_data = {
            "name": "sukurtas",
            "lastname": "test",
        }
        self.quote_form_data = {
            "text": "labadiena",
            "author": self.author1.pk,
        }
        self.quote_invalid_form_data = {
            "text": "labadiena",
            "author": 3,
        }
        self.author_create_url = reverse("author-create")
        self.author_update_url = reverse(
            "author-update", kwargs={"pk": self.author1.pk}
        )
        self.author_delete_url = reverse(
            "author-delete", kwargs={"pk": self.author1.pk}
        )
        self.quote_create_url = reverse("quote-create")
        self.quote_update_url = reverse(
            "quote-update", kwargs={"pk": self.quote1.pk}
        )
        self.quote_delete_url = reverse(
            "quote-delete", kwargs={"pk": self.quote1.pk}
        )

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

        self.client.login(username="test", password="password")

        url = reverse("author-create")
        response = self.client.post(url, data=self.author_form_data)
        created_author = Author.objects.get(name=self.author_form_data["name"])

        self.assertRedirects(response, self.author_list_url)
        self.assertEqual(created_author.name, self.author_form_data["name"])
        self.assertEqual(
            created_author.lastname, self.author_form_data["lastname"]
        )

    def test_author_create_view_redirect_if_not_logged_in(self):
        """Test author create view redirects to login if not logged in"""

        response = self.client.post(
            self.author_create_url, data=self.author_form_data
        )

        # Check if the response redirects to the login page
        self.assertRedirects(
            response, f"/accounts/login/?next={self.author_create_url}"
        )

    def test_author_delete_view(self):
        """test author delete view"""

        self.client.login(username="test", password="password")

        url = reverse("author-delete", kwargs={"pk": self.author1.pk})
        initial_count = Author.objects.count()
        response = self.client.post(url)

        self.assertRedirects(response, self.author_list_url)
        self.assertEqual(Author.objects.count(), initial_count - 1)
        self.assertFalse(Author.objects.filter(pk=self.author1.pk).exists())

    def test_author_delete_view_redirect_if_not_logged_in(self):
        """Test author delete view redirects to login if not logged in"""

        response = self.client.post(
            self.author_delete_url, data=self.author_form_data
        )

        # Check if the response redirects to the login page
        self.assertRedirects(
            response, f"/accounts/login/?next={self.author_delete_url}"
        )

    def test_author_update_view(self):
        """test author update view"""

        self.client.login(username="test", password="password")

        url = reverse("author-update", kwargs={"pk": self.author1.pk})
        response = self.client.post(url, data=self.author_form_data)

        self.assertRedirects(response, self.author_list_url)
        # Refresh the author instance from the database to get the updated data
        self.author1.refresh_from_db()
        self.assertEqual(self.author1.name, self.author_form_data["name"])
        self.assertEqual(
            self.author1.lastname, self.author_form_data["lastname"]
        )

    def test_author_update_view_redirect_if_not_logged_in(self):
        """Test author update view redirects to login if not logged in"""

        response = self.client.post(
            self.author_update_url, data=self.author_form_data
        )

        # Check if the response redirects to the login page
        self.assertRedirects(
            response, f"/accounts/login/?next={self.author_update_url}"
        )

    def test_quote_list_view(self):
        """test quote list view"""

        response = self.client.get(self.quote_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quotes/quote_list.html")
        self.assertIn("object_list", response.context)
        self.assertContains(response, self.quote1.text)
        self.assertContains(response, self.quote2.text)

    def test_quote_list_view_with_query_post(self):
        """test quote list view POST method when there is a query passed in"""

        response = self.client.post(self.quote_list_url, data={"q": "1"})
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the expected quotes
        self.assertContains(response, "Test Quote 1")
        self.assertNotContains(
            response, "Test Quote 2"
        )  # Quote 2 should not be in the response

    def test_quote_list_view_without_query_post(self):
        """test quote list view POST method when there is no query passed in"""

        # Send a POST request without a search query
        response = self.client.post(self.quote_list_url)

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the response contains all quotes
        self.assertContains(response, "Test Quote 1")
        self.assertContains(response, "Test Quote 2")

    def test_quote_detail_view(self):
        """test quote detail view"""

        url = reverse("quote-detail", kwargs={"pk": self.quote1.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quotes/quote_detail.html")
        self.assertContains(response, self.quote1.text)

    def test_quote_create_view_get(self):
        """Test GET request to quote create view"""

        self.client.login(username="test", password="password")

        url = reverse("quote-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quotes/quote_form.html")
        self.assertTrue("form" in response.context)
        self.assertIsInstance(response.context["form"], QuoteForm)

    def test_quote_create_view_post(self):
        """test POST request to quote create view"""

        self.client.login(username="test", password="password")

        url = reverse("quote-create")
        response = self.client.post(url, data=self.quote_form_data)

        self.assertEqual(response.status_code, 302)  # status code for redirect
        self.assertRedirects(response, self.quote_list_url)
        self.assertTrue(
            Quote.objects.filter(
                text=self.quote_form_data["text"], author=self.author1
            ).exists()
        )

    def test_quote_create_view_redirect_if_not_logged_in(self):
        """Test quote create view redirects to login if not logged in"""

        response = self.client.post(
            self.quote_create_url, data=self.quote_form_data
        )

        # Check if the response redirects to the login page
        self.assertRedirects(
            response, f"/accounts/login/?next={self.quote_create_url}"
        )

    def test_quote_create_view_post_invalid_form(self):
        """Test POST request with invalid form data"""

        self.client.login(username="test", password="password")

        url = reverse("quote-create")
        response = self.client.post(url, data=self.quote_invalid_form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quotes/quote_form.html")
        self.assertTrue("form" in response.context)
        self.assertIsInstance(response.context["form"], QuoteForm)
        form = response.context["form"]
        self.assertTrue(form.errors)

    def test_quote_delete_view_get(self):
        """test quote delete view, GET request"""

        self.client.login(username="test", password="password")

        url = reverse("quote-delete", kwargs={"pk": self.quote1.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quotes/quote_confirm_delete.html")

    def test_quote_delete_view_redirect_if_not_logged_in(self):
        """Test quote delete view redirects to login if not logged in"""

        response = self.client.post(
            self.quote_delete_url, data=self.quote_form_data
        )

        # Check if the response redirects to the login page
        self.assertRedirects(
            response, f"/accounts/login/?next={self.quote_delete_url}"
        )

    def test_quote_delete_view_post(self):
        """test quote delete view, POST request"""

        self.client.login(username="test", password="password")

        initial_count = Quote.objects.count()
        url = reverse("quote-delete", kwargs={"pk": self.quote1.pk})
        response = self.client.post(url)

        self.assertFalse(Quote.objects.filter(pk=self.quote1.pk).exists())
        self.assertRedirects(response, self.quote_list_url)
        self.assertEqual(Quote.objects.count(), initial_count - 1)

    def test_quote_update_view(self):
        """test quote update view"""

        self.client.login(username="test", password="password")

        url = reverse("quote-update", kwargs={"pk": self.quote1.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quotes/quote_form.html")
        self.assertTrue("form" in response.context)
        form = response.context["form"]
        self.assertIsInstance(form, QuoteForm)
        self.assertEqual(form["text"].value(), self.quote1.text)

    def test_quote_delete_view_redirect_if_not_logged_in(self):
        """Test quote delete view redirects to login if not logged in"""

        response = self.client.post(
            self.quote_delete_url, data=self.quote_form_data
        )

        # Check if the response redirects to the login page
        self.assertRedirects(
            response, f"/accounts/login/?next={self.quote_delete_url}"
        )

    def test_quote_update_view_get(self):
        """test quote update view, GET request"""

        self.client.login(username="test", password="password")

        url = reverse("quote-update", kwargs={"pk": self.quote1.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quotes/quote_form.html")
        self.assertTrue("form" in response.context)
        self.assertIsInstance(response.context["form"], QuoteForm)

    def test_quote_update_view_post(self):
        """test quote update view, POST request"""

        self.client.login(username="test", password="password")

        url = reverse("quote-update", kwargs={"pk": self.quote1.pk})
        response = self.client.post(url, data=self.quote_form_data)
        updated_quote = Quote.objects.get(pk=self.quote1.pk)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.quote_list_url)
        self.assertEqual(updated_quote.text, self.quote_form_data["text"])
        self.assertEqual(
            updated_quote.author.pk, self.quote_form_data["author"]
        )

    def test_quote_update_view_redirect_if_not_logged_in(self):
        """Test quote update view redirects to login if not logged in"""

        response = self.client.post(
            self.quote_update_url, data=self.quote_form_data
        )

        # Check if the response redirects to the login page
        self.assertRedirects(
            response, f"/accounts/login/?next={self.quote_update_url}"
        )

    def test_quote_update_view_post_invalid(self):
        """Test quote update view with invalid form data, POST request"""

        self.client.login(username="test", password="password")

        url = reverse("quote-update", kwargs={"pk": self.quote1.pk})
        response = self.client.post(url, data=self.quote_invalid_form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quotes/quote_form.html")
        self.assertTrue("form" in response.context)
        form = response.context["form"]
        self.assertIsInstance(form, QuoteForm)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.errors)

        self.assertNotEqual(
            Quote.objects.get(pk=self.quote1.pk).text,
            self.quote_form_data["text"],
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
