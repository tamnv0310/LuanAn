#INSERT PREDICTION to Database BY LASTED
from pymongo import MongoClient, DESCENDING, ReturnDocument
from random import randint
import numpy as np
import pandas as pd
import datetime
import sys
sys.path.append('/Users/nguyenthanhphong/STUDY/SDH/LUAN VAN/air-quality/air-quality-forecast-python/module')

import prediction_2 as prediction

# pprint library is used to make the output look more pretty
from pprint import pprint
import db_config

#Connect to Database Host
client = MongoClient(db_config.getMongoClient())
db = client.air_quality

dist_list = {
    "q1": [10.780612857979111, 106.69929097226942, "Quận 1"],
    "q2": [10.783647660067732, 106.72673471144276,  "Quận 2"],
    "q3": [10.782833128986498, 106.68617895544911,  "Quận 3"],
    "q4": [10.766619604634025, 106.70496162697751,  "Quận 4"],
    "q5": [10.755963008464605, 106.66749108555408,  "Quận 5"],
    "q6": [10.746598181717706, 106.64917765698283,  "Quận 6"],
    "q7": [10.73233643049728, 106.72664202853471,  "Quận 7"],
    "q8": [10.740319883142194, 106.66541075067252,  "Quận 8"],
    "q9": [10.83982108902878, 106.77095208740852,  "Quận 9"],
    "q10": [10.767918838830244, 106.66659593804623,  "Quận 10"],
    "q11": [10.763904275145594, 106.64342383825374,  "Quận 11"],
    "q12": [10.86324605768756, 106.65438133369516,  "Quận 12"],
    "qbthanh": [10.803446284783773, 106.69630236758046, "Q. Bình Thạnh"],
    "qbtan": [10.737193840613681, 106.61566486228712, "Q. Bình Tân"],
    "qgvap": [10.831931525946937, 106.66930567480965, "Q. Gò Vấp"],
    "qpnhuan": [10.795230097898482, 106.67533732496804, "Q. Phú Nhuận"],
    "qtbinh": [10.797934622453923, 106.64237067817248, "Q. Tân Bình"],
    "qtphu": [10.783538492749958, 106.63690663160116, "Q. Tân Phú"],
    "hbchanh": [10.689936987473937, 106.5841934376312, "H. Bình Chánh"],
    "hcgio": [10.411275219925006, 106.95473231899838, "H. Cần Giờ"],
    "hcchi": [10.973555815067174, 106.4938085691552, "H. Củ Chi"],
    "hhmon": [10.889499705704482, 106.59518769231617, "H. Hóc Môn"],
    "hnbe": [10.674384007461548, 106.73295641257327, "Nhà Bè"],
    "tptduc": [10.775752803095694, 106.7544347021429, "TP. Thủ Đức"],
}

product_list = ["no2", "so2", "hcho", "co"]

for product_id in product_list:
    product_id_forecast = product_id+"_forecast"

    print("\n =====> Product id: {0} ~ Product id forecast: {1}".format(product_id, product_id_forecast))

    reconstructed_model = prediction.loadModel(product_id)
    scaler = prediction.loadScaler(product_id)

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
                    _pred_no2 =  {
                                'date': future_date,
                                'dist_id': dist,
                                'val_pred': np.float64(val_pred)
                    }
                    result = db[product_id_forecast].insert_one(_pred_no2)
                    print('Created one {4} prediction {0}_{1} = {3} as id {2}\n'.format(dist, future_date, result.inserted_id, np.float64(val_pred),product_id))
                lasted_doc_saved_value = np.float64(val_pred)
                count = count + 1

        