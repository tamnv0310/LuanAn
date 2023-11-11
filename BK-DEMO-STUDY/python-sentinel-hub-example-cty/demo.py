import matplotlib.pyplot as plt 

from utils import plot_image


from sentinelhub import SentinelHubRequest, SentinelHubDownloadClient, DataCollection, MimeType, DownloadRequest, CRS, BBox, SHConfig, Geometry

#Credentials

CLIENT_ID = '9c688b2a-36c4-4ec7-9a4a-d241edd24ba0'
CLIENT_SECRET = 'RVUHZvYX9av6PIm,]|76<Y8R3*!c%yMr3};LF>hk'
config = SHConfig()

if CLIENT_ID and CLIENT_SECRET:
  config.sh_client_id = CLIENT_ID
  config.sh_client_secret = CLIENT_SECRET
else:
  config = None

evalscript = """
//VERSION=3
//S5P Nitrogen Dioxide (NO2)

var val = NO2;
var minVal = 0.0;
var maxVal = 0.0001;
var diff = maxVal - minVal;
var limits = [
  minVal, 
  minVal + 0.125 * diff, 
  minVal + 0.375 * diff, 
  minVal + 0.625 * diff, 
  minVal + 0.875 * diff, 
  maxVal];
  var colors = [[0, 0, 0.5], [0, 0, 1], [0, 1, 1], [1, 1, 0], [1, 0, 0], [0.5, 0, 0]];
// var colors = ["blue", "lightgreen", "green", "yellow", "orange", "red"];

var ret = colorBlend(val, limits, colors);
ret.push(dataMask);
return ret;
"""
bbox = BBox(bbox=[106.242441, 10.331132, 107.140646, 11.065212], crs=CRS.WGS84)

request = SentinelHubRequest(
  evalscript=evalscript,
  input_data=[
    SentinelHubRequest.input_data(
    data_collection=DataCollection.SENTINEL5P,
    time_interval=('2021-05-09', '2021-05-09'),    
)
  ],
  responses=[
    SentinelHubRequest.output_response('default', MimeType.TIFF),
  ],
  bbox=bbox,  
  size=[512, 425.34],
  config=config
)
response = request.get_data()


# plot_image(response, factor=3.5, clip_range=(0, 1))

print("1233213")
