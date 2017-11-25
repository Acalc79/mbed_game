### import urllib.request if it doesn't work

import urllib.request, json 
response = urllib.request.urlopen('#server url')
data = json.loads(response)
print(data)
    
# or 

import requests
response = requests.get('some url')
print response.json() # if response type is already in json, will automatically get json
    
