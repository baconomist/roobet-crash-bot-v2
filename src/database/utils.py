from pony.orm import Database
import os

import requests


def init_db(db, db_path) -> Database:
    if not os.path.exists(db_path):
        db.bind(provider='sqlite', filename=db_path, create_db=True)
    else:
        db.bind(provider='sqlite', filename=db_path)

    db.generate_mapping(create_tables=True)

    return db

#def bind_db(db, ):


def unbind_db(db):
    db.disconnect()
    db.provider = db.schema = None


def download_latest_db(db, db_path, url) -> Database:
    unbind_db(db)

    latest_db_data = requests.get(url, timeout=2).content
    with open(db_path, "wb") as f:
        f.write(latest_db_data)

    db = init_db(db, db_path)

    return db
