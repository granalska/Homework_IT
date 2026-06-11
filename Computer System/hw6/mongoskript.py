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
    try:
        result = cats_collection.update_one({"name": cat_name}, {"$set": {"age": new_age}})

        if result.matched_count > 0:
            print('Змінено вік')
        else:
            print('Кіт не знайдений')
    except Exception as error:
        print(error)

#додаємо характеристику
def add_cat_feature(cat_name, feature): 
    try:
        result = cats_collection.update_one({"name": cat_name}, {"$push": {"features": feature}})
        
        if result.matched_count > 0:
            print('Додана нова характеристика')
        else:
            print('Помилка додавання')
    except Exception as error:
        print(error)

#мінус кіт
def delete_cat(cat_name):
    try:
        result = cats_collection.delete_one({"name": cat_name})

        if result.matched_count > 0:
            print('Кіт видалений')
        else:
            print('Збігів немає')
    except Exception as error:
        print('error')

#мінус  всі коти
def delete_all_cats():
    try:
        result = cats_collection.delete_many({})

        if result.matched_count > 0:
            print('Коти видалені')
        else:
            print('Збіги відсутні')
    except Exception as error:
        print(error)

cats_collection.insert_one({"_id": ObjectId("60d24b783733b1ae668d4a77"), "name": "Барсік", "age": 3, "features": ["ходить в капці", "дає себе гладити", "рудий"]})
cats_collection.insert_one({"_id": ObjectId("60d24b783733b1ae668d4a78"), "name": "Томас", "age": 2, "features": ["сіро-чорний", "активний", "любить гратися", "бʼє сусідських котів"]})

#перевірка
get_all_cats()
get_cat_by_name("Барсік")
update_cat_age("Барсік", 4)
add_cat_feature("Томас", "любить тунець")