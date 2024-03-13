import json
from bson.objectid import ObjectId

from pymongo import MongoClient

client = MongoClient("mongodb+srv://oleksandr:dnkUq22IrgB7cDyq@cluster0.tgvrxhn.mongodb.net/my_db?retryWrites=true&w=majority&appName=Cluster0")

db = client.dj

with open('quotes.json', 'r') as fd:
    quotes = json.load(fd)


for quote in quotes:
    author = db.authors.find_one({'fullname': quote['author']})
    if author:
        db.quotes.insert_one({
            'quote': quote['quote'],
            'tags': quote['tags'],
            'author': ObjectId(author['_id'])
        })