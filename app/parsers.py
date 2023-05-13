def parse_music_from_db(music) -> dict:
    return {
        "_id": str(music["_id"]),
        "title": music["title"],
        "artist": music["artist"],
        "registration": music["registration"],
    }


def parse_store_from_db(store) -> dict:
    return {
        "_id": str(store["_id"]),
        "music_type": store["music_type"],
    }
