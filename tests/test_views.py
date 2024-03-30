"""File that contains the tests for Django views"""

from django.test import TestCase, Client
from django.urls import reverse


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

    def test_index_get(self):
        """test if the correct template is returned when going to index"""
        response = self.client.get(self.index_url)

        # print(response)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "project/index.html")
