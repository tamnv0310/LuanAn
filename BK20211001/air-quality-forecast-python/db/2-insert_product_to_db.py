#INSERT PRODUCTs to Database in the dataset
from pymongo import MongoClient, DESCENDING
from random import randint
import numpy as np
import pandas as pd

# pprint library is used to make the output look more pretty
from pprint import pprint
import db_config

#Connect to Database Host
client = MongoClient(db_config.getMongoClient())
db = client.air_quality

# Step 2: Create sample data
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

product_list = ["no2", "so2", "hcho", "co", "o3", "ch4"]

# Lay du lieu Quan/Huyen/TP trong dataset
def getDataFile(path_to_csv, from_date=None):
    data = pd.read_csv(path_to_csv)
    if(from_date!=None):
        data_index_from = data[data['date']==from_date].index.values.astype(int)[0]
        _d = data.iloc[data_index_from+1:,:]
        return _d
    return data

for dist in dist_list:
    path_to_dataset = 'air-quality-dataset/_DISTRICT/'+dist+'.csv'
    print("Dataset path: ",path_to_dataset)

    for product_id in product_list:
        lasted_date_saved = None
        for doc in db[product_id].find({'dist_id': dist}).sort([('_id', DESCENDING)]).limit(1):
            lasted_date_saved = doc['date'].strftime('%Y-%m-%d')

        print("District: ", dist," Product: ", product_id)
        print("Last inserted to DB: ", lasted_date_saved)
        dist_data = getDataFile(path_to_dataset, lasted_date_saved)
        print("Dist data records: ", len(dist_data), "\n")

        if(len(dist_data)==0):
            continue

        for index, row in dist_data.iterrows():
            _date = pd.to_datetime(dist_data['date'][index],format='%Y-%m-%d', errors='coerce')
            _val = dist_data[product_id][index]
            if db[product_id].count_documents({'date': _date, 'dist_id': dist}) > 0:
                print('Exist one {2} {0}_{1} in Database'.format(dist, _date, product_id))
                continue
            else:
                print("\nAdding new object to ",dist,"...")
                _doc =  {
                            'date': _date,
                            'dist_id': dist,
                            'val': np.float64(_val)
                        }
                #Step 3: Insert product_id object directly into MongoDB via isnert_one
                result = db[product_id].insert_one(_doc)
                # Step 4: Print to the console the ObjectID of the new document
                print('Created one {4} {0}_{1} = {2} as id {3}'.format(dist, _date, result.inserted_id, np.float64(_val),product_id))





