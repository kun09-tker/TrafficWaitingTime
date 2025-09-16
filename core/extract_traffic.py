from dotenv import load_dotenv
from datetime import datetime

import requests
import os

load_dotenv()
API_KEY_TRAFFIC = os.environ["TRAFFIC_API_KEY"]
API_KEY_WEATHER = os.environ["WEATHER_API_KEY"]

def call_weather_api(lat, lon):
    url = ("https://api.weatherapi.com/v1/current.json"
           f"?key={API_KEY_WEATHER}&q={lat},{lon}")
    response = requests.get(url)
    data = response.json()["current"]
    return data["precip_mm"], \
           data["vis_km"], \
           data["wind_kph"], \
           data["condition"]["text"]

def call_traffic_api(lat, lon):
    url = ("https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
               f"?point={lat},{lon}&unit=KMPH&key={API_KEY_TRAFFIC}")
    response = requests.get(url)
    return response.json()["flowSegmentData"]

def call_api(desc, route_points):
    datas = []
    for lat, lon, distance in route_points:
        data = call_traffic_api(lat, lon)
        data.pop("coordinates", None)
        data["time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        data["distance"] = distance
        data["description"] = desc
        data["latitude"] = lat
        data["longitude"] = lon

        precip_mm, vis_km, wind_kph, condition_text = call_weather_api(lat, lon)

        data["precip_mm"] = precip_mm
        data["vis_km"] = vis_km
        data["wind_kph"] = wind_kph
        data["condition_text"] = condition_text

        datas.append(data)
    return datas