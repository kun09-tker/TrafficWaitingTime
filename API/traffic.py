from dotenv import load_dotenv
from datetime import datetime
from weather import call_weather_api

import database
import requests
import json
import os

load_dotenv()
API_KEY = os.environ["TRAFFIC_API_KEY"]

def call_traffic_api(desc, route_points):

    for lat, lon, distance in route_points:
        url = ("https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
               f"?point={lat},{lon}&unit=KMPH&key={API_KEY}")
        response = requests.get(url)
        data = response.json()["flowSegmentData"]
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

        conn = database.connect_to_database()
        database.create_database(conn)
        database.save_value(conn, data)
        conn.close()
        break

if __name__ == "__main__":
    with open('locations.json', 'r', encoding='utf-8') as f:
        LOCATIONS = json.load(f)["locations"]

    for location in LOCATIONS:
        desc = location["desciption"]
        routes = location["routes"]
        call_traffic_api(desc, routes)
        break