import database
import json
import pandas as pd

from extract_traffic import call_api
from transform_traffic import transform_data
from debug import log_info, log_debug, log_warning, log_error


if __name__ == "__main__":
    try:
        log_info("Bắt đầu chương trình ETL Traffic")

        # Load location
        log_debug("Đang mở file locations.json...")
        with open('locations.json', 'r', encoding='utf-8') as f:
            LOCATIONS = json.load(f)["locations"]
        log_info(f"Đã load {len(LOCATIONS)} locations")

        datas = []

        # Kết nối DB
        log_debug("Kết nối database...")
        conn = database.connect_to_database()
        database.create_database(conn)
        log_info("Đã kết nối và tạo database (nếu chưa có)")

        # Gọi API
        for location in LOCATIONS:
            desc = location["desciption"]
            routes = location["routes"]
            log_debug(f"Gọi API cho location: {desc}, routes={len(routes)}")
            datas.extend(call_api(desc, routes))

        if not datas:
            log_warning("Không có dữ liệu trả về từ API")

        # Lưu raw data
        for data in datas:
            log_debug(f"Lưu dữ liệu gốc: {data}")
            database.save_value(conn, data)
            break
        log_info(f"Đã lưu {len(datas)} bản ghi (raw) vào DB")

        # Transform
        log_debug("Bắt đầu transform dữ liệu...")
        datas = pd.DataFrame(datas)
        datas_transform = transform_data(datas).to_dict(orient="records")
        log_info(f"Đã transform {len(datas_transform)} bản ghi")

        # Lưu transform data
        for data in datas_transform:
            log_debug(f"Lưu dữ liệu transform: {data}")
            database.save_value(conn, data, type='transform')
        log_info(f"Đã lưu {len(datas_transform)} bản ghi (transform) vào DB")

        conn.close()
        log_info("Đã đóng kết nối database")
        log_info("Hoàn tất ETL job ✅")

    except Exception as e:
        log_error(f"Lỗi xảy ra: {e}")
        raise