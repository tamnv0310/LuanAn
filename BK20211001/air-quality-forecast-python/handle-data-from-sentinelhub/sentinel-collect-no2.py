# import matplotlib.pyplot as plt
from sentinelhub import SentinelHubRequest, SentinelHubDownloadClient, DataCollection, MimeType, DownloadRequest, CRS, BBox, SHConfig, Geometry, geometry
import numpy as np
from PIL import Image, ImageFilter
import time
import datetime

# query_date = '2018-05-25'

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

# the evalscript returns NO2 band value
evalscript = """
//VERSON = 3
function setup() {
  return {
    input: ["NO2"],
    output: { bands: 1, sampleType: "FLOAT32" },
    mosaicking: Mosaicking.ORBIT
  };
}

function evaluatePixel(sample) {
  return [sample.NO2];
}
"""

bbox = BBox(bbox=BBoxHoChiMinh, crs=CRS.WGS84)

# Set interval
f = open('air-quality-dataset/log/NO2-log.txt', 'r')
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

  np.savetxt('air-quality-dataset/NO2/NO2-'+query_date +
              '.csv', response_data, delimiter=',')

  log_file = open('air-quality-dataset/log/NO2-log.txt', 'w')
  n = log_file.write(query_date)
  log_file.close()
  
  print("===Saved dataset " + 'NO2-'+query_date + '.csv')

  query_date_temp = query_date
  query_date_temp = datetime.datetime.strptime(
      query_date_temp, '%Y-%m-%d').date() + datetime.timedelta(days=1)
  if query_date_temp >= datetime.datetime.today().date() - datetime.timedelta(days=1):
    break
  query_date = query_date_temp.strftime('%Y-%m-%d')
  time.sleep(2)

# img = Image.fromarray(np.asarray(response_data), 'RGBA').filter(ImageFilter.GaussianBlur(20))
# img.show()

# print("Nitrogen dioxide")
