import requests

req=requests.post(url="http://127.0.0.1:8100/payus/callback/", json={"heading":"passed"})
print(req.json())