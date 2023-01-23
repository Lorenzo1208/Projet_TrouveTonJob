import requests
import pandas as pd

url = "https://raw.githubusercontent.com/Lorenzo1208/Projet_TrouveTonJob/main/data.json"
response = requests.get(url)
data = response.json()

df = pd.DataFrame(data)

print(df)
