import requests

url = "http://127.0.0.1:8000/moderate"
payload = {"text": "fuck these gays lol"}
response = requests.post(url, json=payload)
print(response.status_code)
print(response.text)
