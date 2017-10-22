#!/usr/bin/env python

import requests
import json

resp = requests.get("http://localhost:5000/blockchain")

# error if it didn't work
resp.raise_for_status()

d = resp.json()

print json.dumps(d)
