import pandas as pd
from pymongo import MongoClient, collection
import json
from bson import json_util
import datetime
import numpy as np

import sys
sys.path.append('/Users/nguyenthanhphong/STUDY/SDH/LUAN VAN/air-quality/air-quality-forecast-python/module')

import predict_no2

#Connect to Database Host
client = MongoClient("localhost:27017")
#get Database
db = client.air_quality
#get Collection no2
coll_no2 = db['no2']
coll_no2_pred = db['no2_forecast']
#get Collection district
coll_dist = db.district

def get_no2(district_id=None, from_date=None, to_date=None):
    #Query data ne`
    start = pd.to_datetime(from_date,format='%Y-%m-%d', errors='coerce')
    end = pd.to_datetime(to_date,format='%Y-%m-%d', errors='coerce')
    
    return_data = {
        'dist':{},
        'data': []
    }
    
    retrive_district = coll_dist.find_one({'_id': district_id})
    return_data['dist'] = retrive_district
    real_end = None
    last_val = None

    #if no record
    if(coll_no2.count_documents({'date': {'$gte': start, '$lte': end}, 'dist_id': district_id})==0):
        return_data['data'] = []
        return json.dumps(return_data, indent=4, default=json_util.default, ensure_ascii=False)

    #else, have record(s)
    for doc in coll_no2.find({'date': {'$gte': start, '$lte': end}, 'dist_id': district_id}):
        _d = {
            'date': doc['date'].strftime('%d-%m-%y'),
            'val': doc['val'] * 1000000,
        }
        
        return_data['data'].append(_d)
        real_end = doc['date']
        last_val = doc['val']
    print("Comapre Real end and End: ",real_end, end)

    # if real date above = end date
    if(real_end == end):
        return json.dumps(return_data, indent=4, default=json_util.default, ensure_ascii=False)
    else:
        #predict from real_end to end (not over 7 days)
        count = 1
        future_date = real_end + datetime.timedelta(days=1)
        data_preds = []
        last_val_NEW = last_val
        while future_date < end and count <= 7:
            #find future_date in database
            #if has data
            predict_data = coll_no2_pred.find_one({'date': future_date, 'dist_id': district_id })
            if(predict_data != None):
                print("Predict object ne", predict_data)
                _d = {
                    'date': predict_data['date'].strftime('%d-%m-%y'),
                    'val_pred': predict_data['val_pred'] * 1000000
                }
                data_preds.append(_d)
                last_val_NEW = predict_data['val_pred']
            #if no have data: insert to DB
            else:
                print("Create new object predict base on future_date", last_val_NEW)
                val_pred = predict_no2.predict_from_val(last_val_NEW)
                _pred_no2 =  {
                            'date': future_date,
                            'dist_id': district_id,
                            'val_pred': np.float64(val_pred)
                }
                _d = {
                    'date': future_date.strftime('%d-%m-%y'),
                    'dist_id': district_id,
                    'val_pred': np.float64(val_pred)*1000000
                }
                data_preds.append(_d)
                print("=====Object predict: ", _pred_no2)
                coll_no2_pred.insert_one(_pred_no2)
                # Step 4: Print to the console the ObjectID of the new document
                print('=====Created one predict object')
                last_val_NEW = np.float64(val_pred)

            future_date = future_date + datetime.timedelta(days=1)
            count = count + 1
        return_data['data_pred'] = data_preds
        return json.dumps(return_data, indent=4, default=json_util.default, ensure_ascii=False)

