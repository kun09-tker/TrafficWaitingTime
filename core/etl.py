import database
import json
import pandas as pd

from extract_traffic import call_api
from transform_traffic import transform_data

if __name__ == "__main__":
    with open('locations.json', 'r', encoding='utf-8') as f:
        LOCATIONS = json.load(f)["locations"]
    datas = []

    conn = database.connect_to_database()
    database.create_database(conn)

    for location in LOCATIONS[:1]:
        desc = location["desciption"]
        routes = location["routes"]
        datas.extend(call_api(desc, routes))

    for data in datas:
        database.save_value(conn, data)
        break

    datas = pd.DataFrame(datas)
    datas_transform = transform_data(datas).to_dict(orient="records")
    for data in datas_transform:
        database.save_value(conn, data, type='transform')
    conn.close()