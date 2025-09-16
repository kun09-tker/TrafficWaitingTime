from dotenv import load_dotenv
from datetime import datetime
import requests
import os

from debug import log_info, log_debug, log_warning, log_error

# Load biến môi trường
load_dotenv()
API_KEY_TRAFFIC = os.environ.get("TRAFFIC_API_KEY")
API_KEY_WEATHER = os.environ.get("WEATHER_API_KEY")

if not API_KEY_TRAFFIC:
    log_warning("TRAFFIC_API_KEY không được tìm thấy trong môi trường")
if not API_KEY_WEATHER:
    log_warning("WEATHER_API_KEY không được tìm thấy trong môi trường")


def call_weather_api(lat, lon):
    """Gọi WeatherAPI với tọa độ lat/lon"""
    try:
        url = ("https://api.weatherapi.com/v1/current.json"
               f"?key={API_KEY_WEATHER}&q={lat},{lon}")
        log_debug(f"Weather API request: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json().get("current", {})
        log_info(f"Lấy dữ liệu thời tiết tại ({lat}, {lon}) thành công")

        return (
            data.get("precip_mm", 0.0),
            data.get("vis_km", 0.0),
            data.get("wind_kph", 0.0),
            data.get("condition", {}).get("text", "Unknown")
        )
    except Exception as e:
        log_error(f"Lỗi khi gọi Weather API tại ({lat}, {lon}): {e}")
        return 0.0, 0.0, 0.0, "Error"


def call_traffic_api(lat, lon):
    """Gọi TomTom Traffic API với tọa độ lat/lon"""
    try:
        url = ("https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
               f"?point={lat},{lon}&unit=KMPH&key={API_KEY_TRAFFIC}")
        log_debug(f"Traffic API request: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json().get("flowSegmentData", {})
        log_info(f"Lấy dữ liệu giao thông tại ({lat}, {lon}) thành công")
        return data
    except Exception as e:
        log_error(f"Lỗi khi gọi Traffic API tại ({lat}, {lon}): {e}")
        return {}


def call_api(desc, route_points):
    """Gọi cả Traffic API và Weather API cho các route points"""
    datas = []
    log_info(f"Đang xử lý {len(route_points)} route points cho {desc}")

    for lat, lon, distance in route_points:
        log_debug(f"Xử lý route point: desc={desc}, lat={lat}, lon={lon}, distance={distance}")

        traffic_data = call_traffic_api(lat, lon)
        if not traffic_data:
            log_warning(f"Không có dữ liệu giao thông cho ({lat}, {lon})")
            continue

        # Bổ sung thông tin thêm
        traffic_data.pop("coordinates", None)
        traffic_data["time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        traffic_data["distance"] = distance
        traffic_data["description"] = desc
        traffic_data["latitude"] = lat
        traffic_data["longitude"] = lon

        # Thời tiết
        precip_mm, vis_km, wind_kph, condition_text = call_weather_api(lat, lon)
        traffic_data["precip_mm"] = precip_mm
        traffic_data["vis_km"] = vis_km
        traffic_data["wind_kph"] = wind_kph
        traffic_data["condition_text"] = condition_text

        datas.append(traffic_data)

    log_info(f"Hoàn tất xử lý {len(datas)} dữ liệu cho {desc}")
    return datas
