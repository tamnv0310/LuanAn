# INSERT PRODUCTs to Database in the df
from pymongo import MongoClient, DESCENDING, ReturnDocument
from random import randint
import numpy as np
import pandas as pd

# pprint library is used to make the output look more pretty
from pprint import pprint
import db_config

# Connect to Database Host
client = MongoClient(db_config.getMongoClient())
db = client.air_quality

def getDataFile(path_to_csv, from_date=None):
    data = pd.read_csv(path_to_csv)
    if(from_date != None):
        data_index_from = data[data['date'] == from_date].index.values.astype(int)[
            0]
        _d = data.iloc[data_index_from+1:, :]
        return _d
    return data

path_to_df = 'air-quality/temperature-prediction/manual_db/data/data-pm2.5-lanh-su-quan-hcm-20160211.csv'
print("df path: ", getDataFile(path_to_df))

dist = "q1"
product_id = "pm25"
df = getDataFile(path_to_df, None)
df['date'] = pd.to_datetime(df.date, format='%Y-%m-%d', errors='coerce')
df = df.sort_values(by='date') 

lasted_date_saved = None
for doc in db[product_id].find({'dist_id': 'q1'}).sort([('_id', DESCENDING)]).limit(1):
    lasted_date_saved = pd.to_datetime(doc['date'].strftime('%Y-%m-%d'), format='%Y-%m-%d', errors='coerce')
    print("Last inserted to DB: ", lasted_date_saved)

#neu khong co du lieu nao trong DB
if lasted_date_saved == None:
    lasted_date_saved = "2016-02-11"

for index, row in df.iterrows():
    _date = df['date'][index]

    #neu ngay trong Dataset nho hon ngay luu cuoi cung thi continue
    if(_date <= lasted_date_saved):
        print("Exist record")
        continue
    else:
        print("Create new record")
        _val = df[product_id][index]        

        #Kiem tra lai neu ton tai trong DB thi khong tao moi nua
        if db[product_id].count_documents({'date': _date, 'dist_id': dist}) > 0:
            print('Exist one {0} {1}_{2} in Database'.format(product_id, dist, _date))
            continue
        else:
            print("\nAdding new object to ", product_id, "-", dist, "...")
            _doc = {
                'date': _date,
                'dist_id': dist,
                'val': np.float64(_val),
                'unit': "μg/m3"
            }
            # Step 3: Insert product_id object directly into MongoDB via isnert_one
            result = db[product_id].insert_one(_doc)
            # Step 4: Print to the console the ObjectID of the new document
            print('Created one {0} {1}_{2} = {3} as id {4}'.format(product_id,
                dist, _date, np.float64(_val), result.inserted_id))
