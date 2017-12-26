import json
from pprint import pprint
import urllib.request

data = urllib.request.urlopen('http://api.umd.io/v0/courses/math410/sections')
data = json.load(data)
pprint(data)
