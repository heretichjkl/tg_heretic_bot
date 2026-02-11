from hashlib import md5
from time import time

def get_hash(key: str, seed: str):
    h = md5(
        key.encode('utf-8') + seed.encode('utf-8') + str(time()).encode('utf-8')
    ).hexdigest()

    return h
