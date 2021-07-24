import requests

BASE = "http://127.0.01:5000/"

response = requests.put(BASE + "video/1", data={'name': 'bitcoin', 'views': 100, 'likes': 10})
print(response)
