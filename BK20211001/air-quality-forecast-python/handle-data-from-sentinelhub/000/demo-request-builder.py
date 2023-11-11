
import os
import matplotlib.pyplot as plt
import datetime
BBoxHoChiMinh = [
  106.3555,
  11.157229,
  107.045463,
  10.332237
]


from sentinelhub import SentinelHubRequest, SentinelHubDownloadClient, DataCollection, MimeType, DownloadRequest, CRS, BBox, SHConfig, Geometry

import matplotlib.pyplot as plt

from PIL import Image, ImageFilter


# import os

# dir_path = os.path.dirname(os.path.realpath(__file__))
# hcm_boundary =
# data = Dataset(dir_path + '/' +duong dan den file json')

# Credentials

CLIENT_ID = '9eff5577-8e75-4e4f-9c2c-3940fa4abc79'
CLIENT_SECRET = 'IXp5cK^5[:9>h}5@131:W@SM0npLS0[*<6ZS~A4I'
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
var limits = [minVal, minVal + 0.125 * diff, minVal + 0.375 * diff, minVal + 0.625 * diff, minVal + 0.875 * diff, maxVal];
var colors = [[0, 0, 0.5], [0, 0, 1], [0, 1, 1], [1, 1, 0], [1, 0, 0], [0.5, 0, 0]];

var ret = colorBlend(val, limits, colors);
ret.push(dataMask);
return ret;
"""
bbox = BBox(bbox=BBoxHoChiMinh, crs=CRS.WGS84)

request = SentinelHubRequest(
    evalscript=evalscript,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL5P,
            time_interval=('2021-05-13', '2021-05-13'),
        )
    ],
    responses=[
        SentinelHubRequest.output_response('default', MimeType.TIFF),

    ],
    bbox=bbox,
    size=[512, 425],
    config=config
)
response = request.get_data()

# print(f'Returned data is of type = {type(response)} and length {len(response)}.')
# print(f'Single element in the list is of type {type(response[-1])} and has shape {response[-1].shape}')

# image = response[0]

# print(f'Image type: {image.dtype}')

# # plot function
# # factor 1/255 to scale between 0-1
# # factor 3.5 to increase brightness
# plot_image(image, factor=3.5/255, clip_range=(0,1))

print("abcd")



import numpy as np
# img_w, img_h = 200, 200
# data = np.zeros((img_h, img_w, 3), dtype=np.uint8)
# data[100, 100] = [255, 0, 0]
response_array = np.zeros((512, 425, 4), dtype=np.uint8)
response_array = np.asarray(response[0])
img = Image.fromarray(response_array, 'RGBA')
# img.save('test.png')
img.filter(ImageFilter.GaussianBlur(20)).show()
# img.show()

print("abcdef====", response)
