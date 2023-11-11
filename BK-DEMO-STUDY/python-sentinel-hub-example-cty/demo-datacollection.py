from sentinelhub import SHConfig, BBox, CRS, SentinelHubRequest, MimeType
from sentinelhub import DataCollection

import matplotlib.pyplot as plt

aaaa = DataCollection.SENTINEL5P


# Credentials

CLIENT_ID = '9c688b2a-36c4-4ec7-9a4a-d241edd24ba0'
CLIENT_SECRET = 'RVUHZvYX9av6PIm,]|76<Y8R3*!c%yMr3};LF>hk'
config = SHConfig()

if CLIENT_ID and CLIENT_SECRET:
    config.sh_client_id = CLIENT_ID
    config.sh_client_secret = CLIENT_SECRET
else:
    config = None


# Columbia Glacier, Alaska
glacier_bbox = BBox([-147.8, 60.96, -146.5, 61.38], crs=CRS.WGS84)
glacier_size = (700, 466)
time_interval = '2020-07-15', '2020-07-16'

evalscript_true_color = """
    //VERSION=3

    function setup() {
        return {
            input: [{
                bands: ["B02", "B03", "B04"]
            }],
            output: {
                bands: 3
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B04, sample.B03, sample.B02];
    }
"""

request = SentinelHubRequest(
    evalscript=evalscript_true_color,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L2A,
            time_interval=time_interval,
        )
    ],
    responses=[
        SentinelHubRequest.output_response('default', MimeType.PNG)
    ],
    bbox=glacier_bbox,
    size=glacier_size,
    config=config
)

image = request.get_data()[0]

plt.show(image)

print("321321321")
