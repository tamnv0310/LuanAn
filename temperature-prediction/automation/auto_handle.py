import numpy as np
import pandas as pd
import datetime
import time
import os
from sys import path
from os.path import dirname as dir
import joblib
from datetime import datetime, timedelta

path.append(dir(path[0]) + "/temperature-prediction/automation")
path.append(dir(path[0]) + "/temperature-prediction/module")

# import prediction_2 as prediction

from client_config import *
from csv import writer

from pymongo import MongoClient, DESCENDING, ReturnDocument

import db_config

# from sentinelhub import SentinelHubRequest, DataCollection, MimeType, CRS, BBox, SHConfig

# Connect to Database Host
client = MongoClient(db_config.getMongoClient())
db = client.temperature_predict

# district data
province_list = {
    "binhduong": [11.2741, 106.35879, "Bình Dương", "Dầu Tiếng"],
    "binhphuoc": [11.5354, 106.8832, "Bình Phước", "Đồng Xoài"],
    "vungtau": [10.345, 107.084, "Bà rịa -Vũng Tàu", "Vũng Tàu"],
    "dongnai": [11.2968, 107.084, "Đồng Nai", "Tà Lài"],
    "tayninh": [11.375031, 106.131363, "Tây Ninh", "Tây Ninh"],
    "hcm": [10.787884, 106.698402, "Thành phố Hồ Chí Minh", "Quận 1"],
}

# Credentials (connect Sentinel Hub)
class SHConfig:
    pass


config = SHConfig()

CLIENT_ID = '4529e329-fd65-41ea-b7d3-5705264d39cf'
CLIENT_SECRET = '&T/|3z41kS![}w#Coyp7JLN(d<<Q[hN@FZ,~)1c8'
if CLIENT_ID and CLIENT_SECRET:
    config.sh_client_id = CLIENT_ID
    config.sh_client_secret = CLIENT_SECRET
else:
    config = None


##################
# ADD DATASET
##################


##################
# ADD DATA PROVINCE TO DB
##################
def addProvincesToDB():
    for province in province_list:
        if db.provinces.count_documents({'_id': province}) > 0:
            print('Exist record district {0} in database'.format(province))
            continue
        else:
            _province = {
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
    return ("Added Success")


##################
# ADD DATA TO DB
##################
def addDataToDB():
    collection = db.temperature
    for province in province_list:
        file_path = './module/dataset/' + province + ".csv"
        df = pd.read_csv(file_path)
        df.rename(columns={'MO': 'MONTH', 'DY': 'DAY'}, inplace=True)
        df['DATE'] = pd.to_datetime(df[['YEAR', 'MONTH', 'DAY']])
        df = df.drop(columns=['YEAR', 'MONTH', 'DAY', ]).set_index('DATE')
        temperature_data = []
        for index, row in df.iterrows():
            _temperature = {
                'province_id': province,  #province_id
                'date': index,  # Chuyển đổi index (DATE) thành string
                'val': row.T2M,  # 't2m' là cột chứa giá trị nhiệt độ,
                'isForecast': False
            }
            temperature_data.append(_temperature)

        # Lưu vào MongoDB
        collection.insert_many(temperature_data)

    return ("Added Success")

##################
# ADD DATA TO Predict
##################
def addDataPredictToDB():
    collection = db.temperature
    for province in province_list:
        # Lấy ngày cuối cùng trong collection
        last_date_record = collection.find({'province_id': province}).sort('date', -1).limit(1)
        last_date = list(last_date_record)[0]['date']
        # Tải mô hình
        model_path = './module/models/bayesian_ridge_' + province + "_model.pkl"
        bayes_model = joblib.load(model_path)

        # Lấy ngày hiện tại
        current_date = datetime.now()

        # Tính số ngày cần thêm, bao gồm cả 7 ngày tiếp theo
        days_to_add = (current_date - last_date).days + 7

        # Tạo ngày cho dự đoán
        prediction_dates = [last_date + timedelta(days=i) for i in range(1, days_to_add + 1)]
        temperature_data =[]
        # In kết quả dự đoán
        for date in prediction_dates:
            # Lấy 365 bản ghi cuối cùng
            last_records = collection.find({'province_id': province}).sort('date', -1).limit(365)
            last_records_list = [record['val'] for record in last_records]
            # Tạo dữ liệu đầu vào cho mô hình
            input_data = np.array([last_records_list])
            # Thực hiện dự đoán
            prediction = round(bayes_model.predict(input_data)[0],2)
            _temperature = {
                'province_id': province,  # province_id
                'date': date,  # Chuyển đổi index (DATE) thành string
                'val': prediction,  # 't2m' là cột chứa giá trị nhiệt độ,
                'isForecast': True
            }
            temperature_data.append(_temperature)
            # Lưu vào MongoDB
            collection.insert_one(_temperature)
            print(f"Date: {date.strftime('%Y-%m-%d')}, {prediction}")

    return ("Added Success")

##################
# FUNCTION AUTO RUN EVERY x HOUR
##################
# def autoRunDataEvery(hour: 2):
#     from time import time, sleep
#     while True:
#         # thing to run
#         print("====== START AUTOMATION ======")
#
#         current_moment = datetime.datetime.today()
#         log_txt = "====================\n" + current_moment.strftime('%Y-%m-%d, %H:%M:%S')
#
#         print("\n==> GET DATASET FROM SENTINEL HUB")
#         log_txt = log_txt + "\n==> GET DATASET FROM SENTINEL HUB"
#         collected = sentinelCollectDataset()
#         print(collected)
#         log_txt = log_txt + "\n" + collected
#
#         print("\n==> GET DATASET FROM SENTINEL HUB BY DISTRICT")
#         log_txt = log_txt + "\n==> GET DATASET FROM SENTINEL HUB BY DISTRICT"
#         collected_to_district = sentinelCollectDatasetDistrict()
#         print(collected_to_district)
#         log_txt = log_txt + "\n" + collected_to_district
#
#         print("\n==> ADD NEW AIR QUALITY DATA TO DATABASE")
#         log_txt = log_txt + "\n==> ADD NEW AIR QUALITY DATA TO DATABASE"
#         added_data = addDataToDB()
#         print(added_data)
#         log_txt = log_txt + "\n" + added_data
#
#         print("\n==> ADD NEW AIR QUALITY PREDICT DATA TO DATABASE")
#         log_txt = log_txt + "\n==> ADD NEW AIR QUALITY PREDICT DATA TO DATABASE"
#         added_data_predict = addDataPredictToDB()
#         print(added_data_predict)
#         log_txt = log_txt + "\n" + added_data_predict
#
#         # auto Log
#         log_file = open('air-quality-dataset/log/auto-log.txt', 'w')
#         n = log_file.write(log_txt)
#         log_file.close()
#
#         print("====== END AUTOMATION ======")
#
#         # Flag repeat
#         sleep(60 * 60 * hour - time() % 60)


##################
# AUTO RUN FUNCTIONS EVERY 2 HOUR
##################
# autoRunDataEvery(2)
