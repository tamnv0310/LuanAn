import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageFilter
import datetime
import time

from sentinelhub import SentinelHubRequest, SentinelHubDownloadClient, DataCollection, MimeType, DownloadRequest, CRS, BBox, SHConfig, Geometry

BBoxHoChiMinh = [
    106.3555,
    11.157229,
    107.045463,
    10.332237
]

# Credentials
CLIENT_ID = '29fe609f-24f2-48fd-bb95-f309620a9903'
CLIENT_SECRET = '}|T&GzMu0M.]p-(o~CGd%7X*7@/Ft2!o>uxEEL{)'
config = SHConfig()

if CLIENT_ID and CLIENT_SECRET:
    config.sh_client_id = CLIENT_ID
    config.sh_client_secret = CLIENT_SECRET
else:
    config = None

evalscript = """
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
bbox = BBox(bbox=BBoxHoChiMinh, crs=CRS.WGS84)

# Set interval
f = open('air-quality-dataset/log/O3-log.txt', 'r')
query_date = f.read()
while True:
  print("\n===Query date: " + query_date)
  request = SentinelHubRequest(
      evalscript=evalscript,
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

  np.savetxt('air-quality-dataset/O3/O3-'+query_date +
              '.csv', response_data, delimiter=',')

  log_file = open('air-quality-dataset/log/O3-log.txt', 'w')
  n = log_file.write(query_date)
  log_file.close()
  
  print("===Saved dataset " + 'O3-'+query_date + '.csv')

  query_date_temp = query_date
  query_date_temp = datetime.datetime.strptime(
      query_date_temp, '%Y-%m-%d').date() + datetime.timedelta(days=1)
  if query_date_temp >= datetime.datetime.today().date() - datetime.timedelta(days=1):
    break
  query_date = query_date_temp.strftime('%Y-%m-%d')
  time.sleep(1)

#print("Ozone")