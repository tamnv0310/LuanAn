#INSERT district to DB
from pymongo import MongoClient
from random import randint

# pprint library is used to make the output look more pretty
from pprint import pprint
import db_config

#Connect to Database Host
client = MongoClient(db_config.getMongoClient())
db = client.temperature_prediction

# Step 2: Create sample data
province_list = {
    "binhduong": [11.2741, 106.35879, "Bình Dương", "Dầu Tiếng"],
    "binhphuoc": [11.5354, 106.8832, "Bình Phước", "Đồng Xoài"],
    "vungtau": [10.345, 107.084, "Bà rịa -Vũng Tàu", "Vũng Tàu"],
    "dongnai": [11.2968, 107.084, "Đồng Nai", "Tà Lài"],
    "tayninh": [11.375031, 106.131363, "Tây Ninh", "Tây Ninh"],
    "hcm": [10.787884, 106.698402, "Thành phố Hồ Chí Minh", "Quận 1"],
}

for province in province_list:
    if db.district.count_documents({'_id': province}) > 0:
        print('Exist record district {0} in database'.format(province))
        continue
    else:
        _province =  {
            '_id': province,
            'province_name': province_list[province][2],
            "measuring station": province_list[province][3],
            'location': {
                'lat': province_list[province][0],
                'lon': province_list[province][1]
            }
        }
        # Step 3: Insert district object directly into MongoDB via isnert_one
        result = db.provinces.insert_one(_province)
        # Step 4: Print to the console the ObjectID of the new document
        print('Created {0} as {1}'.format(province, result.inserted_id))

