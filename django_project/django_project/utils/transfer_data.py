import os
import django
from pymongo import MongoClient

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.django_project.settings")
django.setup()

from quotes.models import Tag, Quote, Author

client = MongoClient("mongodb+srv://oleksandr:dnkUq22IrgB7cDyq@cluster0.tgvrxhn.mongodb.net/my_db?retryWrites=true&w=majority&appName=Cluster0")
db = client.dj

# Підключення до бази даних PostgreSQL через Django ORM
from django.db import transaction
from django.db.utils import IntegrityError

@transaction.atomic
def migrate_data():
    authors = db.authors.find()
    for author in authors:
        author_instance, _ = Author.objects.get_or_create(
            fullname=author['fullname'],
            defaults={
                'born_date': author['born_date'],
                'born_location': author['born_location'],
                'description': author['description']
            }
        )

    quotes = db.quotes.find()
    for quote in quotes:
        author_instance = Author.objects.get(fullname=quote['author']['fullname'])
        quote_instance, _ = Quote.objects.get_or_create(
            quote=quote['quote'],
            author=author_instance
        )
        tags = [Tag.objects.get_or_create(name=tag)[0] for tag in quote['tags']]
        quote_instance.tags.add(*tags)

try:
    migrate_data()
    print("Data migration completed successfully.")
except IntegrityError:
    print("Data migration failed due to integrity error.")

