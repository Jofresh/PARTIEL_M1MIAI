from pymongo import MongoClient
from bson import ObjectId

# Database information
MONGO_HOST = "mongodb"
DB_NAME = "store_music"
MUSIC_COLLECTION_NAME = "music"
STORE_COLLECTION_NAME = "store"

client = MongoClient(MONGO_HOST)
db = client[DB_NAME]

# Dictionaries
store = {"_id": ObjectId(), "music_type": "POP"}

# Musics
vinyls = [
    {
        "_id": ObjectId(),
        "title": "Thriller",
        "artist": "Michael Jackson",
        "registration": "MJ281POP0001",
    },
    {
        "_id": ObjectId(),
        "title": "Bad",
        "artist": "Michael Jackson",
        "registration": "MJ213POP0002",
    },
]

dvds = [
    {
        "_id": ObjectId(),
        "title": "A Thousand Miles",
        "artist": "Vanessa Carlton",
        "registration": "VC296POP0003",
    },
    {
        "_id": ObjectId(),
        "title": "I'm Yours",
        "artist": "Jason Mraz",
        "registration": "JM251POP0004",
    },
]

musics = vinyls + dvds

# Inserting data
db[STORE_COLLECTION_NAME].insert_one(store)

db[MUSIC_COLLECTION_NAME].insert_many(musics)

# Adding vinyls and dvds to the created store
db[STORE_COLLECTION_NAME].update_one(
    {"_id": store["_id"]},
    {"$set": {"vinyls": [v["_id"] for v in vinyls], "dvds": [d["_id"] for d in dvds]}},
)
