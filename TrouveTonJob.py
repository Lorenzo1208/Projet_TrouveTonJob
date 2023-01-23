import requests

url = "https://raw.githubusercontent.com/Lorenzo1208/Projet_TrouveTonJob/main/data.json"
response = requests.get(url)
data = response.json()

print(data)
