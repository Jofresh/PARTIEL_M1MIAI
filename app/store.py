from pydantic import BaseModel, validator
from constants import MUSIC_TYPES


class Store(BaseModel):
    music_type: str

    @validator("music_type")
    def music_type_is_valid(cls, v):
        if v not in MUSIC_TYPES:
            raise ValueError("music_type must be a valid music type")
        return v
