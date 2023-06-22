import pymongo
from django.core.management.base import BaseCommand
from Django_site.Stark.StarkApp.models import Author, Quote


class Command(BaseCommand):
    help = 'Migrate data from MongoDB to PostgreSQL'

    def handle(self, *args, **options):
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db = client['mydatabase']
        collection = db['mycollection']

        for document in collection.find():
            author, _ = Author.objects.get_or_create(name=document['author'])
            Quote.objects.create(quote=document['quote'], author=author)
