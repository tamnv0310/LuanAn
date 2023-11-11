import matplotlib.pyplot as pltư
import numpy as np

from utils import plot_image


from sentinelhub import SentinelHubRequest, SentinelHubDownloadClient, DataCollection, MimeType, DownloadRequest, CRS, BBox, SHConfig, Geometry

# Credentials

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
function setup() {
  return {
    input: ["NO2", "dataMask"],
    output: [
        { bands: 1, sampleType: "FLOAT32" }
    ],
    mosaicking: Mosaicking.ORBIT
  }
}

function calculateAverage(samples) {
  var sum = 0;
  var nValid = 0;
  for (let i = 0; i < samples.length; i++) {
    var sample = samples[i];
    if (sample.dataMask != 0) {
      nValid++;
      sum += sample.NO2;
    }
  }
  return sum/nValid;
}

function evaluatePixel(samples) {
    return [calculateAverage(samples)]
}
"""
bbox = BBox(bbox=[106.242441, 10.331132, 107.140646, 11.065212], crs=CRS.WGS84)

request = SentinelHubRequest(
    evalscript=evalscript,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL5P,
            time_interval=('2021-05-10', '2021-05-10'),
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

abcd = np.asarray(response);
print(abcd)

# plot_image(response, factor=3.5, clip_range=(0, 1))

print("1233213")
