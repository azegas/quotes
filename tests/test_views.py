from django.test import TestCase, Client
from django.urls import reverse

from apps.quotes.models import Quote
from apps.authors.models import Author


class TestViews(TestCase):
    def setUp(self):

        '''
        setUp method is simply for creating all kinds of objects that we will
        use/reuse in the tests below, later.
        '''

        self.client = Client()
        self.index_url = reverse('index')

    def test_index_GET(self):
        response = self.client.get(self.index_url)

        # print(response)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "project/index.html")