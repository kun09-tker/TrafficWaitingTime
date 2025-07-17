from dotenv import load_dotenv
import requests
import os

load_dotenv()
API_KEY = os.environ["WEATHER_API_KEY"]

def call_weather_api(lat, lon):
    url = ("https://api.weatherapi.com/v1/current.json"
           f"?key={API_KEY}&q={lat},{lon}")
    response = requests.get(url)
    data = response.json()["current"]
    return data["precip_mm"], \
           data["vis_km"], \
           data["wind_kph"], \
           data["condition"]["text"]

if __name__ == "__main__":
    print(call_weather_api(10.757521087137695, 106.67417724838708))