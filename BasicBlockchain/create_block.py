#!/usr/bin/env python

import requests
import json

d = {
    "from_email": "email2@email.com",
    "to_email": "email1@email.com",
    "amount": 45,
    "contract": "James says this will work",
}

resp = requests.post("http://localhost:5000/block", json=d)

# error if I did this wrong
resp.raise_for_status()

print resp.text

