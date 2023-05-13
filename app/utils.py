def extract_initials_from_artist(artist):
    if len(artist.split()) == 2:
        return "".join([x[0].upper() for x in artist.split(" ")])
    return artist[:2].upper()


def extract_initials_from_music_registration(registration: str):
    return registration[:2]


def extract_music_length_from_music_registration(registration: str):
    return registration[2:5]


def extract_music_type_from_music_registration(registration: str):
    return registration[5:8]


def extract_id_number_from_music_registration(registration: str):
    return registration[8:]
