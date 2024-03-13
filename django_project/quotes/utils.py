from pymongo import MongoClient

def get_mongodb():
    client = MongoClient("mongodb+srv://oleksandr:dnkUq22IrgB7cDyq@cluster0.tgvrxhn.mongodb.net/my_db?retryWrites=true&w=majority&appName=Cluster0")

    db = client.dj

    return db