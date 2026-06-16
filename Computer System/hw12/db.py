from pymongo import MongoClient

client = MongoClient("mongodb://mongo:27017/")
db = client["messages_db"]
collection = db["messages"]

def init_db():
    pass

def save_message(text):
    collection.insert_one({"text": text})

def get_messages():
    return [m["text"] for m in collection.find()]