import os
import json
from django.core.management.base import BaseCommand
from apps.quotes.models import Quote
from apps.authors.models import Author


class Command(BaseCommand):
    help = "Import quotes from a JSON file"

    def handle(self, *args, **kwargs):
        # First, delete all existing quotes and authors
        Quote.objects.all().delete()
        Author.objects.all().delete()

        # Get the directory of the current file
        current_dir = os.path.dirname(__file__)
        # Construct the path to the JSON file
        file_path = os.path.join(current_dir, "quotes.json")

        # Open and read the JSON file
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                author_name = item.get("author")
                if author_name:
                    author, created = Author.objects.get_or_create(
                        name=author_name
                    )
                else:
                    author = None

                Quote.objects.create(
                    text=item["text"],
                    author=author,
                    date_created=item["date_created"],
                )
        self.stdout.write(self.style.SUCCESS("Successfully imported quotes"))
