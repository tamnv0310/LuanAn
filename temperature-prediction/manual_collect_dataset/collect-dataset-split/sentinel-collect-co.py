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

#Credentials

CLIENT_ID = '1c510694-29d2-4094-9d6a-cffe9a8e4274'
CLIENT_SECRET = 'KW|/R[[@{swp5SP8X8&M2*i5C}*5g&7EA2#FCNPv'
config = SHConfig()

if CLIENT_ID and CLIENT_SECRET:
  config.sh_client_id = CLIENT_ID
  config.sh_client_secret = CLIENT_SECRET
else:
  config = None

evalscript = """
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
bbox = BBox(bbox=BBoxHoChiMinh, crs=CRS.WGS84)

# Set interval
f = open('air-quality-dataset/log/CO-log.txt', 'r')
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

  np.savetxt('air-quality-dataset/CO/CO-'+query_date +
              '.csv', response_data, delimiter=',')

  log_file = open('air-quality-dataset/log/CO-log.txt', 'w')
  n = log_file.write(query_date)
  log_file.close()
  
  print("===Saved dataset " + 'CO-'+query_date + '.csv')

  query_date_temp = query_date
  query_date_temp = datetime.datetime.strptime(
      query_date_temp, '%Y-%m-%d').date() + datetime.timedelta(days=1)
  if query_date_temp >= datetime.datetime.today().date() - datetime.timedelta(days=1):
    break
  query_date = query_date_temp.strftime('%Y-%m-%d')
  time.sleep(2)



# request = SentinelHubRequest(
#   evalscript=evalscript,
#   input_data=[
#     SentinelHubRequest.input_data(
#     data_collection=DataCollection.SENTINEL5P,
#     time_interval=('2021-05-19', '2021-05-19'),    
# )
#   ],
#   responses=[
#         SentinelHubRequest.output_response('default', MimeType.TIFF),    
#   ],
#   bbox=bbox,  
#   size=[512, 622.292],
#   config=config
# )
# response = request.get_data() 

# img = Image.fromarray(np.asarray(response[0]), 'RGBA').filter(ImageFilter.GaussianBlur(20))
# img.show()

print("Carbon monoxide")