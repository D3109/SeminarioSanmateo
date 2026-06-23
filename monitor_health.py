import requests
from datetime import datetime

url = "http://localhost:8000/status"

try:
    response = requests.get(url)
    estado = response.status_code
except:
    estado = "ERROR"

with open("log.txt", "a") as f:
    f.write(f"{datetime.now()} - Estado: {estado}\n")