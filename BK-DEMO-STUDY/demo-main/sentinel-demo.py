from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
# Your client credentials
client_id = '56d9a725-c214-4f8d-957b-798dcf5160e1'
client_secret = 'DbPE[~E[j|5KddY7RvItG)k.cx@lI/Mr[.nZ{TZ+'
# Create a session
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)
# Get token for the session
token = oauth.fetch_token(token_url='https://services.sentinel-hub.com/oauth/token',
                          client_id=client_id, client_secret=client_secret)
# All requests using this session will have an access token automatically added
resp = oauth.get("https://services.sentinel-hub.com/oauth/tokeninfo")
print(resp.content)

#==================================

import requests

headers = {
    'Authorization': token,
}

files = {
    'request': (None, '{ "input": { "bounds": { "properties": { "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84" }, "bbox": [ 13, 45, 15, 47 ] }, "data": [ { "type": "S5PL2", "dataFilter": { "timeRange": { "from": "2018-12-30T00:00:00Z", "to": "2018-12-31T00:00:00Z" }, "timeliness": "NRTI" } } ] }, "output": { "width": 512, "height": 512 } }'),
    'evalscript': (None, '//VERSION'),
}

response = requests.post('https://creodias.sentinel-hub.com/api/v1/process', headers=headers, files=files)
