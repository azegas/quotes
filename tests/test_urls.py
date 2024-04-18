"""File that contains the tests for Django urls"""

from django.test import SimpleTestCase
from django.urls import resolve, reverse

from apps.authors.views import AuthorListView


class TestUrls(SimpleTestCase):
    """
    An example test of an url. Not adding more such tests, since they are
    already covered in test_view.py
    """

    def test_author_list_url_is_resolved(self):
        "test for author list url"
        url = reverse("author-list")
        # print(url)
        # print(resolve(url))  # check the output, we use func from it
        resolved_view = resolve(url).func.view_class
        self.assertEqual(resolved_view, AuthorListView)
