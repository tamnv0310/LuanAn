import matplotlib.pyplot as plt 
from 'sentinelhub-py' import SentinelHubRequest, SentinelHubDownloadClient, DataCollection, MimeType, DownloadRequest, CRS, BBox, SHConfig, Geometry

#Credentials

CLIENT_ID = '<your client id here>'
CLIENT_SECRET = '<your client secret here>'
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
    input: ["B02", "B03", "B04"],
    output: { bands: 3 }
  };
}

function evaluatePixel(sample) {
  return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02];
}
"""
bbox = BBox(bbox=[106.521585, 10.352748, 107.053232, 10.911527], crs=CRS.WGS84)

request = SentinelHubRequest(
  evalscript=evalscript,
  input_data=[
    SentinelHubRequest.input_data(
    data_collection=DataCollection.SENTINEL5P,
    time_interval=('2021-04-29', '2021-05-29'),    
)
  ],
  responses=[
    SentinelHubRequest.output_response('default', MimeType.PNG),
    
  ],
  bbox=bbox,  
  size=[512, 547.035],
  config=config
)
response = request.get_data() 