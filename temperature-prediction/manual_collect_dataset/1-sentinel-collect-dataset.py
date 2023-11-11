import numpy as np
import datetime
import time
from client_config import *
import os
# import matplotlib.pyplot as plt
# from PIL import Image, ImageFilter

from sentinelhub import SentinelHubRequest, DataCollection, MimeType, CRS, BBox, SHConfig

BBoxHoChiMinh = [
  106.3555,
  11.157229,
  107.045463,
  10.332237
]

#Credentials

# CLIENT_ID = '1c510694-29d2-4094-9d6a-cffe9a8e4274'
# CLIENT_SECRET = 'KW|/R[[@{swp5SP8X8&M2*i5C}*5g&7EA2#FCNPv'
config = SHConfig()


if CLIENT_ID and CLIENT_SECRET:
  config.sh_client_id = CLIENT_ID
  config.sh_client_secret = CLIENT_SECRET
else:
  config = None


product_list = ["ch4", "co", "hcho", "no2", "o3", "so2"]

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

#for moi chat:
for prod in product_list:
  print("Start get data ", prod)

  query_date = "2018-04-30"
  if(os.path.isfile('air-quality-dataset/log/'+prod+'-log.txt')):
    f = open('air-quality-dataset/log/'+prod+'-log.txt', 'r')
    query_date = f.read()

  while True:
    print("\n===Query date: " + query_date)
    evalscriptMain = None
    if(prod == "ch4"):
      evalscriptMain = evalscript_ch4
    if(prod == "co"):
      evalscriptMain = evalscript_co
    if(prod == "hcho"):
      evalscriptMain = evalscript_hcho
    if(prod == "no2"):
      evalscriptMain = evalscript_no2
    if(prod == "o3"):
      evalscriptMain = evalscript_o3
    if(prod == "so2"):
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

    np.savetxt('air-quality-dataset/'+prod+'/'+prod+'-'+query_date +
                '.csv', response_data, delimiter=',')

    log_file = open('air-quality-dataset/log/'+prod+'-log.txt', 'w')
    n = log_file.write(query_date)
    log_file.close()
    
    print("===Saved " + prod +'-'+query_date + '.csv')

    query_date_temp = query_date
    query_date_temp = datetime.datetime.strptime(
        query_date_temp, '%Y-%m-%d').date() + datetime.timedelta(days=1)
    if query_date_temp >= datetime.datetime.today().date() - datetime.timedelta(days=1):
      break
    query_date = query_date_temp.strftime('%Y-%m-%d')
    time.sleep(2)
  print("Complete ", prod, "\n")