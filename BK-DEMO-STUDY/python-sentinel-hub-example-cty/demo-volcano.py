from sentinelhub import WmsRequest, DataCollection, CRS, BBox, SHConfig

from utils import plot_image

# Credentials

CLIENT_ID = '9c688b2a-36c4-4ec7-9a4a-d241edd24ba0'
CLIENT_SECRET = 'RVUHZvYX9av6PIm,]|76<Y8R3*!c%yMr3};LF>hk'
config = SHConfig()

if CLIENT_ID and CLIENT_SECRET:
    config.sh_client_id = CLIENT_ID
    config.sh_client_secret = CLIENT_SECRET
else:
    config = None   

volcano_bbox = BBox(bbox=[(-2217485.0, 9228907.0), (-2150692.0, 9284045.0)], crs=CRS.POP_WEB)

l2a_request = WmsRequest(
    data_collection=DataCollection.SENTINEL2_L2A,
    layer='TRUE-COLOR-S2-L2A',
    bbox=volcano_bbox,
    time='2017-08-30',
    width=512,
    config=config
)

l2a_data = l2a_request.get_data()
plot_image(l2a_data[0])

print("23213213")