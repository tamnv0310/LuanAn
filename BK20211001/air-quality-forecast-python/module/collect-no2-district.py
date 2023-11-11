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
    "q1": [10.780612857979111, 106.69929097226942],
    "q2": [10.783647660067732, 106.72673471144276],
    "q3": [10.782833128986498, 106.68617895544911],
    "q4": [10.766619604634025, 106.70496162697751],
    "q5": [10.755963008464605, 106.66749108555408],
    "q6": [10.746598181717706, 106.64917765698283],
    "q7": [10.73233643049728, 106.72664202853471],
    "q8": [10.740319883142194, 106.66541075067252],
    "q9": [10.83982108902878, 106.77095208740852],
    "q10": [10.767918838830244, 106.66659593804623],
    "q11": [10.763904275145594, 106.64349224134224],
    "q12": [10.86324605768756, 106.65438133369516],
    "qbthanh": [10.803446284783773, 106.69630236758046],
    "qbtan": [10.737193840613681, 106.61566486228712],
    "qgvap": [10.831931525946937, 106.66930567480965],
    "qpnhuan": [10.795230097898482, 106.67533732496804],
    "qtbinh": [10.797934622453923, 106.64237067817248],
    "qtphu": [10.783538492749958, 106.63690663160116],
    "hbchanh": [10.689936987473937, 106.5841934376312],
    "hcgio": [10.411275219925006, 106.95473231899838],
    "hcchi": [10.973555815067174, 106.4938085691552],
    "hhmon": [10.889499705704482, 106.59518769231617],
    "hnbe": [10.674384007461548, 106.73295641257327],
    "tptduc": [10.775752803095694, 106.7544347021429]
}


def calcPos(loc):
    lat = loc[0]
    lon = loc[1]
    return [round(abs(lat - lat_start)/lat_distance), round(abs(lon - lon_start)/lon_distance)]


def getDataRow(query_date, dist_list, path_to_csv):
    data = np.genfromtxt(path_to_csv, delimiter=',')
    _d = np.array([])

    _d = np.append(_d, query_date)
    count = 0
    for dist in dist_list:
        x = calcPos(dist_list[dist])[0]
        y = calcPos(dist_list[dist])[1]

        count = count + 1
        #neu du lieu la np.nan hoac toa do cac quan khong nam trong TP HCM
        if np.isnan(data[x, y]) or x < 0 or x > row_count-1 or y < 0 or y > row_count-1:
            # print(x,y,0)
            _d = np.append(_d, 0)
        else:
            # print(x,y,data[x,y] * 1000000) #micro mol/m2
            print(x,y,data[x,y],data[x,y]*1000000) #mol/m2
            _d = np.append(_d, data[x, y] * 1000000)  # micro mol/m2
    print("===Added", query_date,",",count," district")
    return _d

def appendRow(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)


# lay du lieu dua vao data set
f = open('air-quality-dataset/log/NO2-district-log.txt', 'r')
query_date = f.read()

while True:
    print("\n===Getting row on: " + query_date)

    path_to_csv = 'air-quality-dataset/NO2/NO2-'+query_date+'.csv'
    
    if os.path.isfile(path_to_csv):

        row_data = getDataRow(query_date, dist_list, path_to_csv)

        # Them vao cuoi file
        appendRow('air-quality-dataset/NO2.csv', row_data)

        log_file = open('air-quality-dataset/log/NO2-district-log.txt', 'w')
        n = log_file.write(query_date)
        log_file.close()

        query_date_temp = query_date
        query_date_temp = datetime.datetime.strptime(
            query_date_temp, '%Y-%m-%d').date() + datetime.timedelta(days=1)
        if query_date_temp >= datetime.datetime.today().date() - datetime.timedelta(days=1):
            break
        query_date = query_date_temp.strftime('%Y-%m-%d')
        time.sleep(2)
    else: 
        print("===File does not exist!")
        break    

print(1111)

#plt.imshow(data, cmap='hot', interpolation='nearest')
# plt.show()
