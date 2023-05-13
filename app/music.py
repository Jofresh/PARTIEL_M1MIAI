from pydantic import BaseModel, validator
from utils import extract_initials_from_artist
from constants import MUSIC_TYPES


class Music(BaseModel):
    title: str
    artist: str
    id: str

    @validator("id")
    def id_is_valid(cls, v, values):
        if len(v) != 12:
            raise ValueError("id must be 12 characters long")

        artist_field = values["artist"]
        artist_initials = extract_initials_from_artist(artist_field)
        music_initials = v[:2]
        if music_initials != artist_initials:
            raise ValueError("id must start with the artist initials")

        music_length = v[2:5]
        if not 60 <= int(music_length) <= 300:
            raise ValueError(
                "id must have a music length between 1 and 5 minutes (60 and 300 seconds)"
            )

        music_type = v[5:8]
        if music_type not in MUSIC_TYPES:
            raise ValueError("id must have a valid music type")

        id_number = v[8:]
        if (not id_number.isdigit()) or "6" in id_number:
            raise ValueError("id identifier must be a number that does not contain a 6")

        return v
