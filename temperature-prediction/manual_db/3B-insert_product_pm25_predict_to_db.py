#INSERT PREDICTION to Database BY LASTED
from pymongo import MongoClient, DESCENDING, ReturnDocument
from random import randint
import numpy as np
import pandas as pd
import datetime

from os.path import dirname as dir
from sys import path
path.append(dir(path[0])+"/module")
import prediction_2 as prediction

# pprint library is used to make the output look more pretty
from pprint import pprint
import db_config

#Connect to Database Host
client = MongoClient(db_config.getMongoClient())
db = client.air_quality

dist_list = {
    "q1": [10.780612857979111, 106.69929097226942, "Quận 1"]
}

product_list = {"pm25":{"model":"rnn-gru"}}

for product_id in product_list:
    product_id_forecast = product_id+"_forecast"
    model_forecast = product_list[product_id]["model"]

    print("\n =====> Product id: {0} ~ Product id forecast: {1}".format(product_id, product_id_forecast))

    reconstructed_model = prediction.loadModel(product_id,model_forecast)
    scaler = prediction.loadScaler(product_id,model_forecast)

    for dist in dist_list:
        lasted_date_saved_date = None
        lasted_doc_saved_value = None

        for doc in db[product_id].find({'dist_id': dist}).sort([('_id', DESCENDING)]).limit(1):
            lasted_doc_saved_date = doc['date']
            lasted_doc_saved_value = doc['val']
            count = 1
            while count <= 7:
                future_date = doc['date'] + datetime.timedelta(days=count)
                print("District: ",dist,"Ngay cuoi actual: ",lasted_doc_saved_date ,"        Ngay moi:", future_date)
                            
                val_pred = prediction.predict_from_val(lasted_doc_saved_value, reconstructed_model, scaler)
                
                doc_future_found = db[product_id_forecast].find_one({'dist_id': dist, 'date' : future_date})
                
                print("Doc future found ",doc_future_found!=None)
                if(doc_future_found!=None):
                    db[product_id_forecast].find_one_and_update({'dist_id': dist, 'date' : future_date}, 
                            { '$set': { "val_pred" : np.float64(val_pred)} }, return_document = ReturnDocument.AFTER)
                    print('Updated one {3} prediction {0}_{1} = {2}\n'.format(dist, future_date, val_pred, product_id))
                else:
                    _predObj =  {
                                'date': future_date,
                                'dist_id': dist,
                                'val_pred': np.float64(val_pred)
                    }
                    result = db[product_id_forecast].insert_one(_predObj)
                    print('Created one {4} prediction {0}_{1} = {3} as id {2}\n'.format(dist, future_date, result.inserted_id, np.float64(val_pred),product_id))
                lasted_doc_saved_value = np.float64(val_pred)
                count = count + 1

        