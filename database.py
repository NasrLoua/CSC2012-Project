from pymongo import MongoClient, errors

from pymongo import MongoClient
def get_database():
    try:
        CONNECTION_STRING = "mongodb+srv://tidus400:s9926139j@psd2.rjbuny6.mongodb.net/?retryWrites=true&w=majority"
    except OperationFailure as e:
        print("Bad Authentication")

    client = MongoClient(CONNECTION_STRING)
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
    }

    user_2 = {
    "_id" : "1",
    "name" : "Egg",
    "username" : "test2",
    "password" : "test2!",
    "points" : 0,
    }

    collection_name.insert_many([user_1,user_2])

def findOneUser(username):
    dbname = get_database()
    collection_name = dbname['profile']
    user = collection_name.find_one({'username': username})
    return user


def addUser(name, username, password):
    dbname = get_database()
    collection_name = dbname ['profile']

    user = {
    "name" : name,
    "username" : username,
    "password" : password,
    "points" : 0,
    }
    collection_name.insert_one(user)

  
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
  
   # Get the database
   dbname = get_database()