from fastapi import FastAPI
from pymongo import MongoClient
from bson import ObjectId

from music import Music
from store import Store

from constants import MUSIC_COLLECTION_NAME, STORE_COLLECTION_NAME, MONGO_HOST, DB_NAME
from parsers import parse_music_from_db, parse_store_from_db
from utils import (
    extract_initials_from_music_registration,
    extract_music_length_from_music_registration,
    extract_music_type_from_music_registration,
    extract_id_number_from_music_registration,
)

client = MongoClient(MONGO_HOST)
db = client[DB_NAME]
app = FastAPI()


# Musics endpoints
@app.get("/musics")
def get_musics():
    musics = db[MUSIC_COLLECTION_NAME].find()

    return [parse_music_from_db(music) for music in musics]


@app.post("/musics")
def create_music(music: Music):
    inserted_music = db[MUSIC_COLLECTION_NAME].insert_one(dict(music))

    return {"_id": str(inserted_music.inserted_id)} | dict(music)


@app.get("/musics/{id}")
def get_music(id: str):
    music = db[MUSIC_COLLECTION_NAME].find_one({"_id": ObjectId(id)})

    if music is None:
        return {"message": "Music not found"}

    return parse_music_from_db(music) | {
        "music_initials": extract_initials_from_music_registration(
            music["registration"]
        ),
        "music_length": extract_music_length_from_music_registration(
            music["registration"]
        ),
        "music_type": extract_music_type_from_music_registration(music["registration"]),
        "music_identifier": extract_id_number_from_music_registration(
            music["registration"]
        ),
    }


@app.put("/musics/{id}")
def update_music(id: str, music: Music):
    existing_music = db[MUSIC_COLLECTION_NAME].find_one({"_id": ObjectId(id)})

    if existing_music is None:
        return {"message": "Music not found"}

    db[MUSIC_COLLECTION_NAME].update_one({"_id": ObjectId(id)}, {"$set": dict(music)})

    return {"_id": id} | dict(music)


@app.delete("/musics/{id}")
def delete_music(id: str):
    music = db[MUSIC_COLLECTION_NAME].find_one({"_id": ObjectId(id)})

    if music is None:
        return {"message": "Music not found"}

    db[MUSIC_COLLECTION_NAME].delete_one({"_id": ObjectId(id)})

    return {"message": "Music deleted"}


# Stores endpoints
@app.get("/stores")
def get_stores():
    stores = db[STORE_COLLECTION_NAME].find()

    return [parse_store_from_db(store) for store in stores]


@app.post("/stores")
def create_store(store: Store):
    inserted_store = db[STORE_COLLECTION_NAME].insert_one(
        dict(store) | {"vinyls": [], "dvds": []}
    )

    return dict(store) | {"_id": str(inserted_store.inserted_id)}


@app.get("/stores/{id}")
def get_store(id: str):
    store = db[STORE_COLLECTION_NAME].find_one({"_id": ObjectId(id)})

    if store is None:
        return {"message": "Store not found"}

    return parse_store_from_db(store) | {
        "vinyls": [str(v) for v in store["vinyls"]],
        "dvds": [str(d) for d in store["dvds"]],
    }


@app.put("/stores/{id}")
def update_store(id: str, store: Store):
    existing_store = db[STORE_COLLECTION_NAME].find_one({"_id": ObjectId(id)})

    if existing_store is None:
        return {"message": "Store not found"}

    db[STORE_COLLECTION_NAME].update_one({"_id": ObjectId(id)}, {"$set": dict(store)})

    return {"_id": id} | dict(store)


@app.delete("/stores/{id}")
def delete_store(id: str):
    store = db[STORE_COLLECTION_NAME].find_one({"_id": ObjectId(id)})

    if store is None:
        return {"message": "Store not found"}

    db[STORE_COLLECTION_NAME].delete_one({"_id": ObjectId(id)})

    return {"message": "Store deleted"}


@app.get("/stores/{store_id}/musics")
def get_store_musics(store_id: str, format: str | None = None):
    store = db[STORE_COLLECTION_NAME].find_one({"_id": ObjectId(store_id)})

    if store is None:
        return {"message": "Store not found"}

    if format is None:
        musics = list(set(store["vinyls"]) | set(store["dvds"]))
    elif format == "vinyls":
        musics = store["vinyls"]
    elif format == "dvds":
        musics = store["dvds"]
    else:
        return {"message": "Invalid format"}

    musics = db[MUSIC_COLLECTION_NAME].find(
        {"_id": {"$in": [ObjectId(m) for m in musics]}}
    )

    return [parse_music_from_db(music) for music in musics]


@app.put("/stores/{store_id}/vinyls/{music_id}")
def add_vinyl_to_store(store_id: str, music_id: str):
    store = db[STORE_COLLECTION_NAME].find_one({"_id": ObjectId(id)})

    if store is None:
        return {"message": "Store not found"}

    music = db[MUSIC_COLLECTION_NAME].find_one({"_id": ObjectId(music_id)})

    if music is None:
        return {"message": "Music not found"}

    music_type = extract_music_type_from_music_registration(music["registration"])

    if store["music_type"] != music_type:
        return {"message": "Music type not compatible for this store"}

    db[STORE_COLLECTION_NAME].update_one(
        {"_id": ObjectId(store_id)}, {"$push": {"vinyls": ObjectId(music_id)}}
    )

    return {"message": "Music added to store"}


@app.delete("/stores/{store_id}/vinyls/{music_id}")
def remove_vinyl_from_store(store_id: str, music_id: str):
    store = db[STORE_COLLECTION_NAME].find_one({"_id": ObjectId(id)})

    if store is None:
        return {"message": "Store not found"}

    if music_id not in store["vinyls"]:
        return {"message": "Music not found"}

    db[STORE_COLLECTION_NAME].update_one(
        {"_id": ObjectId(store_id)}, {"$pull": {"vinyls": ObjectId(music_id)}}
    )

    return {"message": "Music removed from store"}


@app.put("/stores/{store_id}/dvds/{music_id}")
def add_dvd_to_store(store_id: str, music_id: str):
    store = db[STORE_COLLECTION_NAME].find_one({"_id": ObjectId(store_id)})

    if store is None:
        return {"message": "Store not found"}

    music = db[MUSIC_COLLECTION_NAME].find_one({"_id": ObjectId(music_id)})

    if music is None:
        return {"message": "Music not found"}

    music_type = extract_music_type_from_music_registration(music["registration"])

    if store["music_type"] != music_type:
        return {"message": "Music type not compatible for this store"}

    db[STORE_COLLECTION_NAME].update_one(
        {"_id": ObjectId(store_id)}, {"$push": {"dvds": ObjectId(music_id)}}
    )

    return {"message": "Music added to store"}


@app.delete("/stores/{store_id}/dvds/{music_id}")
def remove_dvd_from_store(store_id: str, music_id: str):
    store = db[STORE_COLLECTION_NAME].find_one({"_id": ObjectId(store_id)})

    if store is None:
        return {"message": "Store not found"}

    if music_id not in store["dvds"]:
        return {"message": "Music not found"}

    db[STORE_COLLECTION_NAME].update_one(
        {"_id": ObjectId(store_id)}, {"$pull": {"dvds": ObjectId(music_id)}}
    )

    return {"message": "Music removed from store"}
