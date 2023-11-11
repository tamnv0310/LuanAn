import matplotlib.pyplot as plt

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

    function setup() {
        return {
            input: [{
                bands: ["B02", "B03", "B04"],
                units: "DN"
            }],
            output: {
                bands: 3,
                sampleType: "INT16"
            }
        };
    }

    function updateOutputMetadata(scenes, inputMetadata, outputMetadata) {
        outputMetadata.userData = { "norm_factor":  inputMetadata.normalizationFactor }
    }

    function evaluatePixel(sample) {
        return [sample.B04, sample.B03, sample.B02];
    }
"""

bbox = BBox(bbox=[106.242441, 10.331132, 107.140646, 11.065212], crs=CRS.WGS84)



request_multitype = SentinelHubRequest(
    evalscript=evalscript,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L1C,
            time_interval=('2020-06-01', '2020-06-30'),
            mosaicking_order='leastCC'
        )
    ],
    responses=[
        SentinelHubRequest.output_response('default', MimeType.TIFF),
        SentinelHubRequest.output_response('userdata', MimeType.JSON)
    ],
    bbox=bbox,
    size=[512, 425.34],
    config=config
)

# print out information
multi_data = request_multitype.get_data()[0]
multi_data.keys()

# normalize image
img = multi_data['default.tif']
norm_factor = multi_data['userdata.json']['norm_factor']

img_float32 = img * norm_factor

plot_image(img_float32, factor=3.5, clip_range=(0, 1))


print("0231315646")