# run backups

import json
import pickle
import sys
import os

from flask import Flask, send_file

from pony.orm import *

from database import CrashPoint, db, DB_PATH, init_db
from db_utils import unbind_db

app = Flask(__name__)


@app.route("/get_db")
def database():
    return send_file("database.sqlite")


@app.route("/get_db_trustdice")
def database_trustdice():
    return send_file("database_trustdice.sqlite")


@app.route("/get_most_recent_crash")
def get_most_recent_crash():
    # Reconnect to db
    unbind_db(db)
    init_db(db, DB_PATH)

    @db_session
    def db_query():
        crash_point = select(c for c in CrashPoint).order_by(lambda c: -c.id).limit(1)[0]
        return json.dumps({"crashPoint": crash_point.crash_val, "id": crash_point.api_id})

    return db_query()


@app.route("/get_most_recent_crash_trustdice")
def get_most_recent_crash_trustdice():
    # Reconnect to db
    unbind_db(db)
    dir = __file__.split("\\")
    dir.pop(-1)
    dir = "\\".join(dir)
    db_path = os.path.join(dir, 'database_trustdice.sqlite')
    init_db(db, db_path)

    @db_session
    def db_query():
        crash_point = select(c for c in CrashPoint).order_by(lambda c: -c.id).limit(1)[0]
        return json.dumps({"crashPoint": crash_point.crash_val, "id": crash_point.api_id})

    return db_query()


# TODO: have it check if bot is uploading new data to db by checking db count, if not notify us

if __name__ == "__main__":
    app.run(host=sys.argv[1], debug=True)
