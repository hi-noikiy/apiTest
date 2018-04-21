import pymongo
client = pymongo.MongoClient("192.168.1.75", 27017)
print(client.database_names)
db = client['test']
print(db.collection_names())
