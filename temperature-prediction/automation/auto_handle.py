import numpy as np
import pandas as pd
import datetime
import time
import os
from sys import path
from os.path import dirname as dir

path.append(dir(path[0]) + "/temperature-prediction/automation")
path.append(dir(path[0]) + "/temperature-prediction/module")

# import prediction_2 as prediction

from client_config import *
from csv import writer

from pymongo import MongoClient, DESCENDING, ReturnDocument

import db_config

from sentinelhub import SentinelHubRequest, DataCollection, MimeType, CRS, BBox, SHConfig

# Connect to Database Host
client = MongoClient(db_config.getMongoClient())
db = client.air_quality

# Ho Chi Minh location
BBoxHoChiMinh = [
    106.3555,
    11.157229,
    107.045463,
    10.332237
]

# district data
dist_list = {
    "q1": [10.780612857979111, 106.69929097226942, "Quận 1"],
    "q2": [10.783647660067732, 106.72673471144276, "Quận 2"],
    "q3": [10.782833128986498, 106.68617895544911, "Quận 3"],
    "q4": [10.766619604634025, 106.70496162697751, "Quận 4"],
    "q5": [10.755963008464605, 106.66749108555408, "Quận 5"],
    "q6": [10.746598181717706, 106.64917765698283, "Quận 6"],
    "q7": [10.73233643049728, 106.72664202853471, "Quận 7"],
    "q8": [10.740319883142194, 106.66541075067252, "Quận 8"],
    "q9": [10.83982108902878, 106.77095208740852, "Quận 9"],
    "q10": [10.767918838830244, 106.66659593804623, "Quận 10"],
    "q11": [10.763904275145594, 106.64342383825374, "Quận 11"],
    "q12": [10.86324605768756, 106.65438133369516, "Quận 12"],
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

# product list
product_list = ["ch4", "co", "hcho", "no2", "o3", "so2"]

# Credentials (connect Sentinel Hub)
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
def sentinelCollectDataset():
    evalscript_ch4 = """
  //VERSION=3
  //S5P Methane (CH4)

  function setup() {
    return {
      input: ["CH4"],
      output: { bands: 1, sampleType: "FLOAT32" }
    }
  }

  function evaluatePixel(sample) {
      return [sample.CH4]
  }
  """

    evalscript_co = """
  //VERSION=3
  //S5P Carbon Monoxide (CO)

  function setup() {
    return {
      input: ["CO"],
      output: { bands: 1, sampleType: "FLOAT32" }
    }
  }

  function evaluatePixel(sample) {
      return [sample.CO]
  }
  """

    evalscript_hcho = """
  //VERSION=3
  //S5P Formaldehyde (HCHO)

  function setup() {
    return {
      input: ["HCHO"],
      output: { bands: 1, sampleType: "FLOAT32" }
    }
  }

  function evaluatePixel(sample) {
      return [sample.HCHO]
  }
  """

    evalscript_no2 = """
  //VERSION=3
  //S5P Formaldehyde (HCHO)

  function setup() {
    return {
      input: ["HCHO"],
      output: { bands: 1, sampleType: "FLOAT32" }
    }
  }

  function evaluatePixel(sample) {
      return [sample.HCHO]
  }
  """

    evalscript_o3 = """
  //VERSION=3
  function setup() {
    return {
      input: ["O3", "dataMask"],
      output: { bands: 1 , sampleType: "FLOAT32" },
    }
  }

  function evaluatePixel(sample) {
    return [sample.O3]
  }
  """

    evalscript_so2 = """
  //VERSION=3
  //S5P Sulfur Dioxide (SO2)

  function setup() {
    return {
      input: ["SO2"],
      output: { bands: 1, sampleType: "FLOAT32" }
    }
  }

  function evaluatePixel(sample) {
      return [sample.SO2]
  }
  """

    bbox = BBox(bbox=BBoxHoChiMinh, crs=CRS.WGS84)
    msg = ''
    # for moi chat:
    for prod in product_list:
        print("Start get data ", prod)
        query_date = "2018-04-30"
        if (os.path.isfile('air-quality-dataset/log/' + prod + '-log.txt')):
            f = open('air-quality-dataset/log/' + prod + '-log.txt', 'r')
            query_date = f.read()

        while True:
            print("\n===Query date: " + query_date)
            evalscriptMain = None
            if (prod == "ch4"):
                evalscriptMain = evalscript_ch4
            if (prod == "co"):
                evalscriptMain = evalscript_co
            if (prod == "hcho"):
                evalscriptMain = evalscript_hcho
            if (prod == "no2"):
                evalscriptMain = evalscript_no2
            if (prod == "o3"):
                evalscriptMain = evalscript_o3
            if (prod == "so2"):
                evalscriptMain = evalscript_so2

            request = SentinelHubRequest(
                evalscript=evalscriptMain,
                input_data=[
                    SentinelHubRequest.input_data(
                        data_collection=DataCollection.SENTINEL5P,
                        time_interval=(query_date, query_date),
                    )
                ],
                responses=[
                    SentinelHubRequest.output_response('default', MimeType.TIFF),
                ],
                bbox=bbox,
                size=[512, 425.34],
                config=config
            )
            response_data = request.get_data()[0]

            np.savetxt('air-quality-dataset/' + prod + '/' + prod + '-' + query_date +
                       '.csv', response_data, delimiter=',')

            log_file = open('air-quality-dataset/log/' + prod + '-log.txt', 'w')
            n = log_file.write(query_date)
            log_file.close()

            print("===Saved " + prod + '-' + query_date + '.csv')

            query_date_temp = query_date
            query_date_temp = datetime.datetime.strptime(
                query_date_temp, '%Y-%m-%d').date() + datetime.timedelta(days=1)
            if query_date_temp >= datetime.datetime.today().date() - datetime.timedelta(days=1):
                break
            query_date = query_date_temp.strftime('%Y-%m-%d')
            time.sleep(2)
        msg = msg + ' ' + prod
        print("Complete ", prod, "\n")

    return ("Collected until " + query_date + ':' + msg)


##################
# ADD DATASET BY DISTRICT
##################
def sentinelCollectDatasetDistrict():
    msg = ''
    hcm = {
        "tl": [BBoxHoChiMinh[1], BBoxHoChiMinh[0]],
        "br": [BBoxHoChiMinh[3], BBoxHoChiMinh[2]]
    }
    row_count = 425
    col_count = 512

    lat_start = hcm["tl"][0]
    lon_start = hcm["tl"][1]
    lat_end = hcm["br"][0]
    lon_end = hcm["br"][1]

    lat_distance = abs(lat_start - lat_end) / row_count
    lon_distance = abs(lon_start - lon_end) / col_count

    dist_list = {
        # "distname": [lat, lon, x, y],
        "q1": [10.780612857979111, 106.69929097226942, 194, 255],
        "q2": [10.783647660067732, 106.72673471144276, 192, 275],
        "q3": [10.782833128986498, 106.68617895544911, 193, 245],
        "q4": [10.766619604634025, 106.70496162697751, 201, 259],
        "q5": [10.755963008464605, 106.66749108555408, 207, 232],
        "q6": [10.746598181717706, 106.64917765698283, 212, 218],
        "q7": [10.73233643049728, 106.72664202853471, 219, 275],
        "q8": [10.740319883142194, 106.66541075067252, 215, 230],
        "q9": [10.83982108902878, 106.77095208740852, 164, 308],
        "q10": [10.767918838830244, 106.66659593804623, 201, 231],
        "q11": [10.763904275145594, 106.64342383825374, 203, 214],
        "q12": [10.86324605768756, 106.65438133369516, 151, 222],
        "qbthanh": [10.803446284783773, 106.69630236758046, 182, 253],
        "qbtan": [10.737193840613681, 106.61566486228712, 216, 193],
        "qgvap": [10.831931525946937, 106.66930567480965, 168, 233],
        "qpnhuan": [10.795230097898482, 106.67533732496804, 186, 237],
        "qtbinh": [10.797934622453923, 106.64237067817248, 185, 213],
        "qtphu": [10.783538492749958, 106.63690663160116, 193, 209],
        "hbchanh": [10.689936987473937, 106.5841934376312, 241, 170],
        "hcgio": [10.411275219925006, 106.95473231899838, 384, 445],
        "hcchi": [10.973555815067174, 106.4938085691552, 95, 103],
        "hhmon": [10.889499705704482, 106.59518769231617, 138, 178],
        "hnbe": [10.674384007461548, 106.73295641257327, 249, 280],
        "tptduc": [10.775752803095694, 106.7544347021429, 197, 296]
    }

    col_head_list = {"1": "date", "2": "dist", "3": "co",
                     "4": "no2", "5": "o3", "6": "so2", "8": "hcho"}

    # Lay du lieu Quan/Huyen/TP trong dataset
    def getDataFile(path_to_csv):
        data = np.genfromtxt(path_to_csv, delimiter=',')
        return data

    # Lay du lieu mot vi tri Quan/Huyen/TP trong dataset
    def getVal(data, x, y):
        # neu du lieu la np.nan hoac toa do cac quan khong nam trong TP HCM
        if np.isnan(data[x, y]) or (data[x, y] < 0) or (x < 0) or (x > row_count - 1) or (y < 0) or (y > row_count - 1):
            # print(x,y,0)
            return 0
        else:
            return data[x, y]

    # them du lieu vao 1 dong trong dataset
    def appendRow(file_name, d_row):
        # Open file in append mode
        with open(file_name, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(d_row)

    # ============================
    # === BAT DAU CHUONG TRINH ===
    # ============================

    # Tao file data set
    for dist in dist_list:
        # neu KHONG ton tai file dataset ==> tao file dataset
        path_to_dataset = 'air-quality-dataset/_DISTRICT/' + dist + '.csv'
        if os.path.isfile(path_to_dataset) == False:
            col_head_array = []
            for col in col_head_list:
                col_head_array.append(col_head_list[col])
            np.savetxt(path_to_dataset, [col_head_array], delimiter=',', fmt='%s')

    # Them du lieu vao cac dataset cua 24 quan/huyen/tp
    query_date = "2018-04-30"
    if (os.path.isfile('air-quality-dataset/log/district-log.txt')):
        f = open('air-quality-dataset/log/district-log.txt', 'r')
        query_date = f.read()

    while True:
        print("\n===Getting data on: " + query_date)

        path_to_csv_co = 'air-quality-dataset/CO/CO-' + query_date + '.csv'
        path_to_csv_no2 = 'air-quality-dataset/NO2/NO2-' + query_date + '.csv'
        path_to_csv_o3 = 'air-quality-dataset/O3/O3-' + query_date + '.csv'
        path_to_csv_so2 = 'air-quality-dataset/SO2/SO2-' + query_date + '.csv'
        path_to_csv_ch4 = 'air-quality-dataset/CH4/CH4-' + query_date + '.csv'
        path_to_csv_hcho = 'air-quality-dataset/HCHO/HCHO-' + query_date + '.csv'

        if os.path.isfile(path_to_csv_co):
            print("accept")
        else:
            return ("Lasted records were added.")

        data_co = getDataFile(path_to_csv_co)
        data_no2 = getDataFile(path_to_csv_no2)
        data_o3 = getDataFile(path_to_csv_o3)
        data_so2 = getDataFile(path_to_csv_so2)
        data_ch4 = getDataFile(path_to_csv_ch4)
        data_hcho = getDataFile(path_to_csv_hcho)

        # them du lieu vao cac file dataset quan/huyen
        for dist in dist_list:
            path_to_dataset = 'air-quality-dataset/_DISTRICT/' + dist + '.csv'

            # Kiem tra da ton tai trong csv
            # chua lam

            # ngay, Quan/Huyen/TP, CO, NO2, O3, SO2, CH4, HCHO
            datarow = [query_date, dist, 0, 0, 0, 0, 0, 0]
            print(data_co)
            if os.path.isfile(path_to_csv_co):
                datarow[2] = getVal(data_co, dist_list[dist][2], dist_list[dist][3])
            else:
                break
            if os.path.isfile(path_to_csv_no2):
                datarow[3] = getVal(data_no2, dist_list[dist][2], dist_list[dist][3])
            else:
                break
            if os.path.isfile(path_to_csv_o3):
                datarow[4] = getVal(data_o3, dist_list[dist][2], dist_list[dist][3])
            else:
                break
            if os.path.isfile(path_to_csv_so2):
                datarow[5] = getVal(data_so2, dist_list[dist][2], dist_list[dist][3])
            else:
                break
            if os.path.isfile(path_to_csv_ch4):
                datarow[6] = getVal(data_ch4, dist_list[dist][2], dist_list[dist][3])
            else:
                break
            if os.path.isfile(path_to_csv_hcho):
                datarow[7] = getVal(data_hcho, dist_list[dist][2], dist_list[dist][3])
            else:
                break

            # Them vao cuoi file
            appendRow(path_to_dataset, datarow)

        print("===Added 24 districts on ", query_date)

        # ghi lai log sau khi them vao 1 row cua 24 quan/huyen
        log_file = open('air-quality-dataset/log/district-log.txt', 'w')
        query_date_temp = query_date
        query_date_temp = datetime.datetime.strptime(query_date_temp, '%Y-%m-%d').date() + datetime.timedelta(days=1)
        # if query_date_temp >= datetime.datetime.today().date() - datetime.timedelta(days=1):
        #     break
        query_date = query_date_temp.strftime('%Y-%m-%d')
        n = log_file.write(query_date)
        print("Logged file", query_date)
        log_file.close()
        time.sleep(0.125)
        if query_date_temp >= datetime.datetime.today().date() - datetime.timedelta(days=1):
            break
    return ("Add success until " + query_date)


##################
# ADD DATA DISTRICT TO DB
##################
def addDistrictToDB():
    for dist in dist_list:
        if db.district.count_documents({'_id': dist}) > 0:
            print('Exist record district {0} in database'.format(dist))
            continue
        else:
            _district = {
                '_id': dist,
                'dist_name': dist_list[dist][2],
                'location': {
                    'lat': dist_list[dist][0],
                    'lon': dist_list[dist][1]
                }
            }
            # Step 3: Insert district object directly into MongoDB via isnert_one
            result = db.district.insert_one(_district)
            # Step 4: Print to the console the ObjectID of the new document
            print('Created {0} as {1}'.format(dist, result.inserted_id))
    return ("Added Success")


##################
# ADD DATA TO DB (WITHOUT CH4)
##################
def addDataToDB():
    # product list WITHOUT CH4
    product_list = ["co", "hcho", "no2", "o3", "so2"]

    # Lay du lieu Quan/Huyen/TP trong dataset
    def getDataFile(path_to_csv, from_date=None):
        data = pd.read_csv(path_to_csv)
        if (from_date != None):
            data_index_from = data[data['date'] == from_date].index.values.astype(int)[0]
            _d = data.iloc[data_index_from + 1:, :]
            return _d
        return data

    for dist in dist_list:
        path_to_dataset = 'air-quality-dataset/_DISTRICT/' + dist + '.csv'
        print("Dataset path: ", path_to_dataset)

        for product_id in product_list:
            lasted_date_saved = None
            for doc in db[product_id].find({'dist_id': dist}).sort([('_id', DESCENDING)]).limit(1):
                lasted_date_saved = doc['date'].strftime('%Y-%m-%d')

            # neu khong co du lieu nao trong DB
            if lasted_date_saved == None:
                lasted_date_saved = "2018-04-30"

            print("District: ", dist, " Product: ", product_id)
            print("Last inserted to DB: ", lasted_date_saved)
            dist_data = getDataFile(path_to_dataset, lasted_date_saved)
            print("Dist data records: ", len(dist_data), "\n")

            if (len(dist_data) == 0):
                continue

            for index, row in dist_data.iterrows():
                _date = pd.to_datetime(dist_data['date'][index], format='%Y-%m-%d', errors='coerce')
                _val = dist_data[product_id][index]
                if db[product_id].count_documents({'date': _date, 'dist_id': dist}) > 0:
                    print('Exist one {2} {0}_{1} in Database'.format(dist, _date, product_id))
                    continue
                else:
                    print("\nAdding new object to ", dist, "...")
                    _doc = {
                        'date': _date,
                        'dist_id': dist,
                        'val': np.float64(_val)
                    }
                    # Step 3: Insert product_id object directly into MongoDB via isnert_one
                    result = db[product_id].insert_one(_doc)
                    # Step 4: Print to the console the ObjectID of the new document
                    print('Created one {4} {0}_{1} = {3} as id {2}'.format(dist, _date, result.inserted_id,
                                                                           np.float64(_val), product_id))
    return ("Added Success")


##################
# ADD DATA PREDICT TO DB (WITHOUT CH4)
##################
def addDataPredictToDB():
    product_list = {
        "no2": {"model": "rnn-lstm"},
        "so2": {"model": "rnn-gru"},
        "hcho": {"model": "rnn-gru"},
        "co": {"model": "rnn-gru"},
        "o3": {"model": "rnn-lstm"}
    }

    # for product_id in product_list:
    #     product_id_forecast = product_id+"_forecast"
    #     model_forecast = product_list[product_id]["model"]
    #
    #     print("\n =====> Product id: {0} ~ Product id forecast: {1}".format(
    #         product_id, product_id_forecast))
    #
    #     reconstructed_model = prediction.loadModel(product_id,model_forecast)
    #     scaler = prediction.loadScaler(product_id,model_forecast)
    #
    #     for dist in dist_list:
    #         lasted_date_saved_date = None
    #         lasted_doc_saved_value = None
    #
    #         for doc in db[product_id].find({'dist_id': dist}).sort([('_id', DESCENDING)]).limit(1):
    #             lasted_doc_saved_date = doc['date']
    #             lasted_doc_saved_value = doc['val']
    #             count = 1
    #             while count <= 7:
    #                 future_date = doc['date'] + datetime.timedelta(days=count)
    #                 print("District: ", dist, "Ngay cuoi actual: ",
    #                       lasted_doc_saved_date, " - Ngay moi:", future_date)
    #
    #                 val_pred = prediction.predict_from_val(
    #                     lasted_doc_saved_value, reconstructed_model, scaler)
    #
    #                 doc_future_found = db[product_id_forecast].find_one(
    #                     {'dist_id': dist, 'date': future_date})
    #
    #                 print("Doc future found ", doc_future_found != None)
    #                 if(doc_future_found != None):
    #                     db[product_id_forecast].find_one_and_update({'dist_id': dist, 'date': future_date},
    #                                                                 {'$set': {"val_pred": np.float64(val_pred)}}, return_document=ReturnDocument.AFTER)
    #                     print('Updated one {0} prediction {0}_{1} = {2} by {4}\n'.format(
    #                         product_id, dist, future_date, val_pred, model_forecast))
    #                 else:
    #                     _predObj = {
    #                         'date': future_date,
    #                         'dist_id': dist,
    #                         'val_pred': np.float64(val_pred)
    #                     }
    #                     result = db[product_id_forecast].insert_one(_predObj)
    #                     print('Created one {0} prediction {1}_{2} = {3} as id {4} by {5}\n'.format(
    #                         product_id, dist, future_date, np.float64(val_pred),result.inserted_id, model_forecast))
    #                 lasted_doc_saved_value = np.float64(val_pred)
    #                 count = count + 1
    # return ("Added Success")


##################
# FUNCTION AUTO RUN EVERY x HOUR
##################
def autoRunDataEvery(hour: 2):
    from time import time, sleep
    while True:
        # thing to run
        print("====== START AUTOMATION ======")

        current_moment = datetime.datetime.today()
        log_txt = "====================\n" + current_moment.strftime('%Y-%m-%d, %H:%M:%S')

        print("\n==> GET DATASET FROM SENTINEL HUB")
        log_txt = log_txt + "\n==> GET DATASET FROM SENTINEL HUB"
        collected = sentinelCollectDataset()
        print(collected)
        log_txt = log_txt + "\n" + collected

        print("\n==> GET DATASET FROM SENTINEL HUB BY DISTRICT")
        log_txt = log_txt + "\n==> GET DATASET FROM SENTINEL HUB BY DISTRICT"
        collected_to_district = sentinelCollectDatasetDistrict()
        print(collected_to_district)
        log_txt = log_txt + "\n" + collected_to_district

        print("\n==> ADD NEW AIR QUALITY DATA TO DATABASE")
        log_txt = log_txt + "\n==> ADD NEW AIR QUALITY DATA TO DATABASE"
        added_data = addDataToDB()
        print(added_data)
        log_txt = log_txt + "\n" + added_data

        print("\n==> ADD NEW AIR QUALITY PREDICT DATA TO DATABASE")
        log_txt = log_txt + "\n==> ADD NEW AIR QUALITY PREDICT DATA TO DATABASE"
        added_data_predict = addDataPredictToDB()
        print(added_data_predict)
        log_txt = log_txt + "\n" + added_data_predict

        # auto Log
        log_file = open('air-quality-dataset/log/auto-log.txt', 'w')
        n = log_file.write(log_txt)
        log_file.close()

        print("====== END AUTOMATION ======")

        # Flag repeat
        sleep(60 * 60 * hour - time() % 60)


##################
# AUTO RUN FUNCTIONS EVERY 2 HOUR
##################
# autoRunDataEvery(2)
