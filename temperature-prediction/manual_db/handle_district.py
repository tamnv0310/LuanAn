import pandas as pd
from pymongo import MongoClient, collection
import json
from bson import json_util

#Connect to Database Host
client = MongoClient("localhost:27017")
#get Database
db = client.air_quality
#get Collection district
coll_dist = db.district

def get_all():
    return_data = []
    for doc in coll_dist.find():
        return_data.append(doc)
        print(doc)
    return json.dumps(return_data, indent=4, default=json_util.default, ensure_ascii=False)