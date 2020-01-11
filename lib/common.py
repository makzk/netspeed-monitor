import settings
from pymongo import MongoClient

db = None


def get_database():
    global db
    if db is None:
        mongo_client = MongoClient(settings.DATABASE_URI)
        db = mongo_client.get_default_database()
    return db


def size_scale(n_bytes):
    units = ['', 'k', 'm', 'g', 't']
    times = 0
    scaled_size = n_bytes + 0
    while times < len(units):
        if abs(scaled_size) < 1000:
            break
        scaled_size /= 1024
        times += 1

    return '{:.2f}{}bps'.format(scaled_size, units[times])
