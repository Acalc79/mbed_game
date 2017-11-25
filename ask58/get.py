import requests
r = requests.get('some url')
print r.json() # if response type is already in json, will automatically get json

#or 

### import urllib.request if it doesn't work

import urllib.request, json 
with urllib.request.urlopen(" #server url ") as url:
    data = json.loads(url.read().decode())
    print(data)
    
