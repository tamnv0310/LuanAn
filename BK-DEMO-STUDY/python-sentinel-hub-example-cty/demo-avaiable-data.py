from sentinelhub import SentinelHubRequest, SentinelHubDownloadClient, DataCollection, MimeType, DownloadRequest, CRS, BBox, SHConfig, Geometry, SentinelHubCatalog

import matplotlib.pyplot as plt

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


catalog = SentinelHubCatalog(config=config)

catalog.get_info()

print(catalog.get_info())