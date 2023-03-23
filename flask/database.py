from flask import request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from pymongo import MongoClient,errors
import pymongo
from bson import ObjectId

def get_database():
    try:
        CONNECTION_STRING = "mongodb+srv://test:hOzAAWFmWthTqsg6@psd2.rjbuny6.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(CONNECTION_STRING)
    except OperationFailure as e:
        print("Bad Authentication")
    return client['recycling']

def insertDummy():
    dbname = get_database()
    collection_name = dbname ['profile']

    user_1 = {
    "_id" : "0",
    "name" : "Blender",
    "username" : "test1",
    "password" : "test1!",
    "points" : 0,
    "profile_pic":"/static/generic_profile_pic.png"
    }

    user_2 = {
    "_id" : "1",
    "name" : "Egg",
    "username" : "test2",
    "password" : "test2!",
    "points" : 0,
    "profile_pic":"/static/generic_profile_pic.png"
    }

    collection_name.insert_many([user_1,user_2])

def findOneUser(username):
    dbname = get_database()
    collection_name = dbname['profile']
    user = collection_name.find_one({'username': username})
    return user

def findOneVoucher(id):
    dbname = get_database()
    collection_name = dbname['vouchers']
    voucher = collection_name.find_one({'_id': ObjectId(id)})
    return voucher


def addUser(name, username, password):
    dbname = get_database()
    collection_name = dbname ['profile']

    user = {
    "name" : name,
    "username" : username,
    "password" : password,
    "points" : 0,
    "profile_pic":"/static/profile_pics/generic_profile_pic.png"
    }
    collection_name.insert_one(user)

def incrementPoints(username, points):
    dbname = get_database()
    collection_name = dbname ['profile']
    collection_name.update_one({'username': username}, {'$inc': {'points': points}})


def changeProfilePic(username,filename):
    dbname = get_database()
    collection_name = dbname['profile']
    collection_name.update_one({'username': username}, {'$set': {'profile_pic': '/static/profile_pics/' + filename}})


def getAllOrderByPoints():
    dbname = get_database()
    collection_name = dbname['profile']
    x = collection_name.find().sort('points', pymongo.DESCENDING)
    return x

def getAllVouchers():
    dbname = get_database()
    collection_name = dbname['vouchers']
    x = collection_name.find()
    return x

# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
  
   # Get the database
   dbname = get_database()