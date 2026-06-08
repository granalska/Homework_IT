from pymongo import MongoClient
from bson import ObjectId

mongo_connection = MongoClient("mongodb://localhost:27017/")
database = mongo_connection["cats_database"]
cats_collection = database["Котики"]

#всі коти
def get_all_cats():
    for cat in cats_collection.find():
        print(cat)

#імʼя
def get_cat_by_name(cat_name):
    print(cats_collection.find_one({"name": cat_name}))

#міняємо вік
def update_cat_age(cat_name, new_age):
    cats_collection.update_one({"name": cat_name}, {"$set": {"age": new_age}})

#додаємо характеристику
def add_cat_feature(cat_name, feature):
    cats_collection.update_one({"name": cat_name}, {"$push": {"features": feature}})

#мінус кіт
def delete_cat(cat_name):
    cats_collection.delete_one({"name": cat_name})

#мінус  всі коти
def delete_all_cats():
    cats_collection.delete_many({})

cats_collection.insert_one({"_id": ObjectId("60d24b783733b1ae668d4a77"), "name": "Барсік", "age": 3, "features": ["ходить в капці", "дає себе гладити", "рудий"]})
cats_collection.insert_one({"_id": ObjectId("60d24b783733b1ae668d4a78"), "name": "Томас", "age": 2, "features": ["сіро-чорний", "активний", "любить гратися", "бʼє сусідських котів"]})

#перевірка
get_all_cats()
get_cat_by_name("Барсік")
update_cat_age("Барсік", 4)
add_cat_feature("Томас", "любить тунець")