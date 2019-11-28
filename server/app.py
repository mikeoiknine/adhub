import schedule
import datetime
from flask import Flask

from flask.json import JSONEncoder

from . import create_app
from bson import json_util
from .db import mongo

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj): return json_util.default(obj)

app = create_app()
app.json_encoder = CustomJSONEncoder


def resetStats():
    day_of_month = datetime.datetime.now().day
    year = datetime.datetime.now().year
    mongo.db.advertisements.update(
        {},
        {"$set": {'stats.day_view_count': 0}},
        upsert=False
    )

    if day_of_month == 1:
        mongo.db.advertisements.update(
            {},
            {"$set": {'stats.month_view_count': 0}},
            upsert=False
        )

    if year != current_year:
        mongo.db.advertisements.update(
            {},
            {"$set": {'stats.year_view_count': 0}},
            upsert=False
        )


current_year = 2019
schedule.every().day.do(resetStats)


