import pymongo
from pymongo import MongoClient
from datetime import datetime

import csv, os

class MongoViews:


    MONGO_VIEW_ANDROID_REVIEWS = "test_btc"

class MongoManager:

    DBURL = "mongodb://127.0.0.1:27017"
    # DBURL = 'mongodb://utapass-jenkins.kkinternal.com:27017'

    client = None
    db = None

    def __init__(self):
        self.client = MongoClient(self.DBURL)
        self.db = self.client['kevin']
        return None



    def BTC_existed(self,data):

        col = MongoViews.MONGO_VIEW_ANDROID_REVIEWS
        collection = self.db[col]
        result = collection.find_one( {"name":  data['name']

                                   })
        return result['price']

    def insert_reviews (self, data):
        col = MongoViews.MONGO_VIEW_ANDROID_REVIEWS
        collection = self.db[col]
        result = collection.insert_one(
                {
                    "name" : data['name'],
                    "price": data['price']
                })

    def update_score(self, data):
        col = MongoViews.MONGO_VIEW_ANDROID_REVIEWS
        collection = self.db[col]
        if data['name']=="BTC":
            result = collection.update_one({"name" : "BTC"}, {"$set":{ "price" : data['price']}})
            if not result.raw_result['updatedExisting']: collection.insert_one({ "name" : "BTC", "price" : data['price']})
        else:
            result = collection.update_one({"name" : "LTC"}, {"$set":{ "price" : data['price']}})
            if not result.raw_result['updatedExisting']: collection.insert_one({ "name" : "LTC", "price" : data['price']})







