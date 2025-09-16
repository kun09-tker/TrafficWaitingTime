import pandas as pd
from debug import log_info, log_warning, log_error


def map_waiting(x):
    if x <= 300:
        return 'Chờ không đáng kể'
    elif x <= 600:
        return 'Chờ chấp nhận được'
    else:
        return 'Chờ lâu'


def map_period(h):
    if 6 <= h < 8:
        return 'Sáng'
    elif 8 <= h < 12:
        return 'Trưa'
    elif 12 <= h < 17:
        return 'Chiều'
    else:
        return 'Ngoài khung'


def map_distance(d):
    if d <= 200:
        return 'Gần'
    elif d <= 500:
        return 'Trung bình'
    else:
        return 'Xa'


def map_time_slot(h):
    if 6 <= h < 8:
        return '6:00 - 8:00'
    elif 8 <= h < 12:
        return '11:00 - 12:00'
    elif 12 <= h < 17:
        return '16:00 - 17:00'
    else:
        return 'Ngoài khung'


def map_precip(mm):
    if mm <= 0:
        return 'Không mưa (0)'
    elif mm <= 2.5:
        return 'Mưa nhẹ (0 - 2.5)'
    else:
        return 'Mưa lớn (> 2.5)'


def map_wind(w):
    if w <= 10:
        return 'Yên lặng (< 11)'
    elif w <= 20:
        return 'Gió vừa (11 - 20)'
    else:
        return 'Gió mạnh (> 20)'


def map_vis(v):
    if v <= 5:
        return 'Thấp (< 6)'
    elif v <= 10:
        return 'Trung bình (6 - 10)'
    else:
        return 'Cao (> 10)'


def transform_data(df):
    log_info("Bắt đầu transform dữ liệu")
    df = df.copy()

    try:
        df['time'] = pd.to_datetime(df['time'])
        df['delay_time'] = df['currentTravelTime'] - df['freeFlowTravelTime']
        df['waiting'] = df['delay_time'].apply(map_waiting)
        df['hour'] = df['time'].dt.hour
        df['date'] = df['time'].dt.date

        before = len(df)
        df_filtered = df.dropna(subset=['delay_time', 'roadClosure'])
        df_filtered = df_filtered[df_filtered['delay_time'] >= 0]
        df_filtered = df_filtered[df_filtered['roadClosure'] == False]
        after = len(df_filtered)

        log_info(f"Lọc dữ liệu: {before} → {after}")

        df_filtered['period'] = df_filtered['hour'].apply(map_period)
        df_filtered['distance_bin'] = df_filtered['distance'].apply(map_distance)
        df_filtered['time_slot'] = df_filtered['hour'].apply(map_time_slot)
        df_filtered['precip_mm_bin'] = df_filtered['precip_mm'].apply(map_precip)
        df_filtered['wind_kph_bin'] = df_filtered['wind_kph'].apply(map_wind)
        df_filtered['vis_km_bin'] = df_filtered['vis_km'].apply(map_vis)

        # Scale tọa độ an toàn
        lon_min, lon_max = df['longitude'].min(), df['longitude'].max()
        lat_min, lat_max = df['latitude'].min(), df['latitude'].max()

        if lon_min == lon_max or lat_min == lat_max:
            log_warning("Không thể scale tọa độ do toàn bộ giá trị bằng nhau")
            df_filtered['x_img'] = 0
            df_filtered['y_img'] = 0
        else:
            lon_scale = (df["longitude"] - lon_min) / (lon_max - lon_min)
            lat_scale = (df["latitude"] - lat_min) / (lat_max - lat_min)
            df_filtered['x_img'] = 689 * lon_scale.round(2) * 0.8 + 78
            df_filtered['y_img'] = 516 * (1 - lat_scale.round(2)) * 0.8 + 78

        log_info("Hoàn tất transform dữ liệu")
        return df_filtered

    except Exception as e:
        log_error(f"Lỗi khi transform dữ liệu: {e}")
        raise
