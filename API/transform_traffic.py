import database
import pandas as pd
import numpy as np

WEATHER_MAPPING = {
    "Clear": "Quang đãng",
    "Cloudy": "Nhiều mây",
    "Light rain": "Mưa nhẹ",
    "Light rain shower": "Mưa rào nhẹ",
    "Moderate rain": "Mưa vừa",
    "Moderate rain at times": "Thỉnh thoảng mưa vừa",
    "Overcast": "U ám",
    "Partly Cloudy": "Trời ít mây",
    "Partly cloudy": "Trời ít mây",
    "Patchy light drizzle": "Mưa phùn rải rác nhẹ",
    "Patchy rain nearby": "Có mưa rải rác gần đó",
    "Sunny": "Nắng"
}


def transform_data(df):
    df['time'] = pd.to_datetime(df['time'])  # Chuyển time thành datetime
    df['delay_time'] = df['currenttraveltime'] - df['freeflowtraveltime']  # Tính delay
    df['hour'] = df['time'].dt.hour  # Trích giờ để lọc khung
    df['date'] = df['time'].dt.date
    # Lọc dữ liệu cho 3 khung giờ
    df_filtered = df[df['hour'].isin([6, 7, 11, 12, 16])]

    df_filtered = df_filtered.dropna()  # Loại null nếu có
    df_filtered = df_filtered[df_filtered['delay_time'] >= 0]  # Loại delay âm
    df_filtered = df_filtered[df_filtered['roadclosure'] == False]  # Loại đường đóng

    # Nhóm distance thành categorical cho association rules
    df_filtered['distance_bin'] = pd.cut(df_filtered['distance'],
                                         bins=[0, 200, 500, float('inf')],
                                         labels=['Gần', 'Trung bình', 'Xa'])
    # Mã hóa thời tiết và khung giờ
    df_filtered['time_slot'] = pd.cut(df_filtered['hour'],
                                      bins=[6, 8, 12, 17],
                                      labels=['6:00 - 7:59', '11:00 - 12:00', '16:00 - 17:00'],
                                      right=False)
    df_filtered['condition_text'] = df_filtered['condition_text'].astype('category')
    df_filtered['condition_text_vn'] = df_filtered['condition_text'].map(WEATHER_MAPPING)


    df_filtered['precip_mm_bin'] = pd.cut(df_filtered['precip_mm'],
                                        bins=[-float('inf'), 0, 2.5, float('inf')],
                                        labels=['Không mưa (0)', 'Mưa nhẹ (0 - 2.5)', 'Mưa lớn (> 2.5)'],
                                        right=True)
    df_filtered['wind_kph_bin'] = pd.cut(df_filtered['wind_kph'],
                                        bins=[-float('inf'), 10, 20, float('inf')],
                                        labels=['Yên lặng (< 11)', 'Gió vừa (11 - 20)', 'Gió mạnh (> 20)'],
                                        right=True)
    df_filtered['vis_km_bin'] = pd.cut(df_filtered['vis_km'],
                                   bins=[0, 5, 10, float('inf')],
                                   labels=['Thấp (< 6)', 'Trung bình (6 - 10)', 'Cao (> 10)'],
                                   right=True)

    lon_scale = (df["longitude"] - df["longitude"].min()) / \
                (df["longitude"].max() - df["longitude"].min())
    lat_scale = (df["latitude"] - df["latitude"].min()) / \
                (df["latitude"].max() - df["latitude"].min())
    lon_scale = round(lon_scale.astype(float), 2)
    lat_scale = round(lat_scale.astype(float), 2)
    df_filtered['x_img'] = 689 * (lon_scale) * 0.8 + 78
    df_filtered['y_img'] = 516 * (1 - lat_scale) * 0.8 + 78

    return df_filtered

def get_all_weather(df):
    category = df['condition_text_vn'].unique()
    max_delay_time = float(df['delay_time'].max())
    return category, max_delay_time

if __name__ == "__main__":
    conn = database.connect_to_database()
    df = database.fetch_data(conn)
    df = transform_data(df)
    df.to_csv('transform_traffic_data.csv', index=False)
    conn.close()

