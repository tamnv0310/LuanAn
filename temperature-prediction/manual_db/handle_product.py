import pandas as pd
from pymongo import MongoClient, collection
import json
from bson import json_util
import datetime
import numpy as np

from os.path import dirname as dir
from sys import path
path.append(dir(path[0])+"/temperature-prediction/module")

# import prediction

#Connect to Database Host
client = MongoClient("localhost:27017")
#get Database
db = client.air_quality
#get Collection district
coll_dist = db.district

#Get data by Product, District ID, Date range
def get_data(product_id=None, district_id=None, from_date=None, to_date=None):
    #get Collection
    coll = db[product_id]
    coll_pred = db[product_id+'_forecast']
    coefficient = 1000000
    if product_id == "pm25":
        coefficient = 1

    #Query data:
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
    if(coll.count_documents({'date': {'$gte': start, '$lte': end}, 'dist_id': district_id})==0):
        return_data['data'] = []
        return json.dumps(return_data, indent=4, default=json_util.default, ensure_ascii=False)

    #else, have record(s)
    for doc in coll.find({'date': {'$gte': start, '$lte': end}, 'dist_id': district_id}):
        _d = {
            'date': doc['date'].strftime('%d-%m-%y'),
            'val': doc['val'] * coefficient,
        }
        
        return_data['data'].append(_d)
        real_end = doc['date']
        last_val = doc['val']
    print("Compare Real end and End: ",real_end, end)

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
            predict_data = coll_pred.find_one({'date': future_date, 'dist_id': district_id })
            if(predict_data != None):
                print("Predict object ne", predict_data)
                _d = {
                    'date': predict_data['date'].strftime('%d-%m-%y'),
                    'val_pred': round(predict_data['val_pred'] * coefficient, 2)
                }
                data_preds.append(_d)
                last_val_NEW = predict_data['val_pred']
            #if no have data: insert to DB
            else:
                print("Create new object predict base on future_date", last_val_NEW)
                val_pred = prediction.predict_from_val(product_id, last_val_NEW)
                _pred_no2 =  {
                            'date': future_date,
                            'dist_id': district_id,
                            'val_pred': np.float64(val_pred)
                }
                _d = {
                    'date': future_date.strftime('%d-%m-%y'),
                    'dist_id': district_id,
                    'val_pred': round(np.float64(val_pred)*coefficient, 2)
                }
                data_preds.append(_d)
                print("=====Object predict: ", _pred_no2)
                coll_pred.insert_one(_pred_no2)
                # Step 4: Print to the console the ObjectID of the new document
                print('=====Created one predict object')
                last_val_NEW = np.float64(val_pred)

            future_date = future_date + datetime.timedelta(days=1)
            count = count + 1
        return_data['data_pred'] = data_preds
        return json.dumps(return_data, indent=4, default=json_util.default, ensure_ascii=False)

#Get data by Product, District ID, Date range
def get_data_file(product_id=None, district_id=None, from_date=None, to_date=None):
    #get Collection
    coll = db[product_id]
    coll_pred = db[product_id+'_forecast']
    coefficient = 1000000
    if product_id == "pm25":
        coefficient = 1

    #Query data:
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
    if(coll.count_documents({'date': {'$gte': start, '$lte': end}, 'dist_id': district_id})==0):
        return_data['data'] = []
        return json.dumps(return_data, indent=4, default=json_util.default, ensure_ascii=False)

    #else, have record(s)
    for doc in coll.find({'date': {'$gte': start, '$lte': end}, 'dist_id': district_id}):
        _d = {
            'date': doc['date'].strftime('%d-%m-%y'),
            'val': doc['val'] * coefficient,
        }
        
        return_data['data'].append(_d)
        real_end = doc['date']
        last_val = doc['val']
    print("Compare Real end and End: ",real_end, end)

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
            predict_data = coll_pred.find_one({'date': future_date, 'dist_id': district_id })
            if(predict_data != None):
                print("Predict object ne", predict_data)
                _d = {
                    'date': predict_data['date'].strftime('%d-%m-%y'),
                    'val_pred': round(predict_data['val_pred'] * coefficient, 2)
                }
                data_preds.append(_d)
                last_val_NEW = predict_data['val_pred']
            #if no have data: insert to DB
            else:
                print("Create new object predict base on future_date", last_val_NEW)
                val_pred = prediction.predict_from_val(product_id, last_val_NEW)
                _pred_no2 =  {
                            'date': future_date,
                            'dist_id': district_id,
                            'val_pred': np.float64(val_pred)
                }
                _d = {
                    'date': future_date.strftime('%d-%m-%y'),
                    'dist_id': district_id,
                    'val_pred': round(np.float64(val_pred)*coefficient, 2)
                }
                data_preds.append(_d)
                print("=====Object predict: ", _pred_no2)
                coll_pred.insert_one(_pred_no2)
                # Step 4: Print to the console the ObjectID of the new document
                print('=====Created one predict object')
                last_val_NEW = np.float64(val_pred)

            future_date = future_date + datetime.timedelta(days=1)
            count = count + 1
        return_data['data_pred'] = data_preds
        return json.dumps(return_data, indent=4, default=json_util.default, ensure_ascii=False)

#Get data by Product, one Date
def get_data_all_dist(product_id=None,dt=None):
    print("====Info get_data_all_dist", product_id, dt,pd.to_datetime(dt,format='%Y-%m-%d', errors='coerce'))
    #get Collection
    coll = db[product_id]
    coefficient = 1000000
    if product_id == "pm25":
        coefficient = 1
    # coll_pred = db[product_id+'_forecast']

    return_data = {
        'query_date': dt,
        'product_id': product_id,
        'data': {}
    }

    #Query data:
    query_date = pd.to_datetime(dt,format='%Y-%m-%d', errors='coerce')
    for doc in coll.find({'date': query_date}):
        # _d = {
        #     'dist_id': doc['dist_id'],
        #     'val': doc['val'] * 1000000,
        # }
        print(doc['dist_id'])
        return_data['data'][doc['dist_id']] = doc['val'] * coefficient

    return json.dumps(return_data, indent=4, default=json_util.default, ensure_ascii=False)

#Get data forecast by Product, one Date
def get_data_predict_all_dist(product_id=None,dt=None):
    print("====Info get_data_predict_all_dist", product_id, dt,pd.to_datetime(dt,format='%Y-%m-%d', errors='coerce'))
    #get Collection
    coll_pred = db[product_id+"_forecast"]
    # coll_pred = db[product_id+'_forecast']
    coefficient = 1000000
    if product_id == "pm25":
        coefficient = 1
    return_data = {
        'query_date': dt,
        'product_id': product_id,
        'data': {}
    }

    #Query data:
    query_date = pd.to_datetime(dt,format='%Y-%m-%d', errors='coerce')
    for doc in coll_pred.find({'date': query_date}):
        print(doc['dist_id'])
        return_data['data'][doc['dist_id']] = doc['val_pred'] * coefficient

    return json.dumps(return_data, indent=4, default=json_util.default, ensure_ascii=False)