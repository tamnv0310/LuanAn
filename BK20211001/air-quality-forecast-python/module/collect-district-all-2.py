from textwrap import wrap
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time
import numpy as np
from csv import writer
import os

hcm = {
    "tl": [11.157229, 106.3555],
    "br": [10.332237, 107.045463]
}
row_count = 425
col_count = 512

lat_start = hcm["tl"][0]
lon_start = hcm["tl"][1]
lat_end = hcm["br"][0]
lon_end = hcm["br"][1]

lat_distance = abs(lat_start - lat_end)/row_count
lon_distance = abs(lon_start - lon_end)/col_count

dist_list = {
    # "distname": [lat, lon, x, y, no],
    "q1": [10.780612857979111, 106.69929097226942, 194, 255, 1],
    "q2": [10.783647660067732, 106.72673471144276, 192, 275, 2],
    "q3": [10.782833128986498, 106.68617895544911, 193, 245, 3],
    "q4": [10.766619604634025, 106.70496162697751, 201, 259, 4],
    "q5": [10.755963008464605, 106.66749108555408, 207, 232, 5],
    "q6": [10.746598181717706, 106.64917765698283, 212, 218, 6],
    "q7": [10.73233643049728, 106.72664202853471, 219, 275, 7],
    "q8": [10.740319883142194, 106.66541075067252, 215, 230, 8],
    "q9": [10.83982108902878, 106.77095208740852, 164, 308, 9],
    "q10": [10.767918838830244, 106.66659593804623, 201, 231, 10],
    "q11": [10.763904275145594, 106., 203, 214, 11],
    "q12": [10.86324605768756, 106.65438133369516, 151, 222, 12],
    "qbthanh": [10.803446284783773, 106.69630236758046, 182, 253, 13],
    "qbtan": [10.737193840613681, 106.61566486228712, 216, 193, 14],
    "qgvap": [10.831931525946937, 106.66930567480965, 168, 233, 15],
    "qpnhuan": [10.795230097898482, 106.67533732496804, 186, 237, 16],
    "qtbinh": [10.797934622453923, 106.64237067817248, 185, 213, 17],
    "qtphu": [10.783538492749958, 106.63690663160116, 193, 209, 18],
    "hbchanh": [10.689936987473937, 106.5841934376312, 241, 170, 19],
    "hcgio": [10.411275219925006, 106.95473231899838, 384, 445, 20],
    "hcchi": [10.973555815067174, 106.4938085691552, 95, 103, 21],
    "hhmon": [10.889499705704482, 106.59518769231617, 138, 178, 22],
    "hnbe": [10.674384007461548, 106.73295641257327, 249, 280, 23],
    "tptduc": [10.775752803095694, 106.7544347021429, 197, 296, 24]
}

col_head_list = {"1": "date", "2": "dist", "3": "co",
                 "4": "no2", "5": "o3", "6": "so2", "7": "ch4", "8": "hcho", "9": "dist_id"}

# Lay du lieu mot vi tri Quan/Huyen/TP trong dataset
def getDataFile(path_to_csv):
    data = np.genfromtxt(path_to_csv, delimiter=',')
    return data

def getVal(data, x, y):
    # neu du lieu la np.nan hoac toa do cac quan khong nam trong TP HCM
    if np.isnan(data[x, y]) or (data[x,y] < 0) or (x < 0) or (x > row_count-1) or (y < 0) or (y > row_count-1):
        # print(x,y,0)
        return 0
    else:
        return data[x, y]

#them du lieu vao 1 dong trong dataset
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

# neu KHONG ton tai file dataset ==> tao file dataset
path_to_dataset = 'air-quality-dataset/_DISTRICT-ALL/hcm-2.csv'
if os.path.isfile(path_to_dataset) == False:
    col_head_array = []
    for col in col_head_list:
        col_head_array.append(col_head_list[col])
    np.savetxt(path_to_dataset, [col_head_array], delimiter=',', fmt='%s')
    
#Them du lieu vao cac dataset cua 24 quan/huyen/tp
f = open('air-quality-dataset/log/district-all-log-2.txt', 'r')
query_date = f.read()

while True:
    print("\n===Getting data on: " + query_date)

    path_to_csv_co = 'air-quality-dataset/CO/CO-'+query_date+'.csv'
    path_to_csv_no2 = 'air-quality-dataset/NO2/NO2-'+query_date+'.csv'
    path_to_csv_o3 = 'air-quality-dataset/O3/O3-'+query_date+'.csv'
    path_to_csv_so2 = 'air-quality-dataset/SO2/SO2-'+query_date+'.csv'
    path_to_csv_ch4 = 'air-quality-dataset/CH4/CH4-'+query_date+'.csv'
    path_to_csv_hcho = 'air-quality-dataset/HCHO/HCHO-'+query_date+'.csv'

    data_co = getDataFile(path_to_csv_co)
    data_no2 = getDataFile(path_to_csv_no2)
    data_o3 = getDataFile(path_to_csv_o3)
    data_so2 = getDataFile(path_to_csv_so2)
    data_ch4 = getDataFile(path_to_csv_ch4)
    data_hcho = getDataFile(path_to_csv_hcho)

    #them du lieu vao cac file dataset quan/huyen/tp
    for dist in dist_list:
        path_to_dataset = 'air-quality-dataset/_DISTRICT-ALL/hcm-2.csv'

        # Kiem tra da ton tai trong csv
        # chua lam

        # ngay, Quan/Huyen/TP, CO, NO2, O3, SO2, CH4, HCHO , dist_id 
        datarow = [query_date, dist, 0, 0, 0, 0, 0 ,0, dist_list[dist][4]]    
        if os.path.isfile(path_to_csv_co):
            datarow[2] = getVal(data_co, dist_list[dist][2], dist_list[dist][3])
        else:
            break
        if os.path.isfile(path_to_csv_no2):
            datarow[3]= getVal(data_no2, dist_list[dist][2], dist_list[dist][3])
        else:
            break
        if os.path.isfile(path_to_csv_o3):
            datarow[4]= getVal(data_o3, dist_list[dist][2], dist_list[dist][3])
        else:
            break
        if os.path.isfile(path_to_csv_so2):
            datarow[5]= getVal(data_so2, dist_list[dist][2], dist_list[dist][3])
        else:
            break
        if os.path.isfile(path_to_csv_ch4):
            datarow[6]= getVal(data_ch4, dist_list[dist][2], dist_list[dist][3])
        else:
            break
        if os.path.isfile(path_to_csv_hcho):
            datarow[7]= getVal(data_hcho, dist_list[dist][2], dist_list[dist][3])
        else:
            break

        # Them vao cuoi file
        appendRow(path_to_dataset, datarow)

    print("===Added 24 districts on ", query_date)

    #ghi lai log sau khi them vao 1 row cua 24 q/h/tp
    log_file = open('air-quality-dataset/log/district-all-log-2.txt', 'w')
    

    query_date_temp = query_date
    query_date_temp = datetime.datetime.strptime(query_date_temp, '%Y-%m-%d').date() + datetime.timedelta(days=1)
    if query_date_temp >= datetime.datetime.today().date() - datetime.timedelta(days=1):
        break
    query_date = query_date_temp.strftime('%Y-%m-%d')
    n = log_file.write(query_date)
    log_file.close()

    time.sleep(0.125)
