import pandas as pd

def map_waiting(x):
    if x <= 300:
        return 'Chờ không đáng kể'
    elif x <= 600:
        return 'Chờ chấp nhận được'
    else:
        return 'Chờ lâu'

# period: theo hour
def map_period(h):
    if 6 <= h < 8:
        return 'Sáng'
    elif 8 <= h < 12:
        return 'Trưa'
    elif 12 <= h < 17:
        return 'Chiều'
    else:
        return None

# distance_bin
def map_distance(d):
    if d <= 200:
        return 'Gần'
    elif d <= 500:
        return 'Trung bình'
    else:
        return 'Xa'

# time_slot: theo hour
def map_time_slot(h):
    if 6 <= h < 8:
        return '6:00 - 8:00'
    elif 8 <= h < 12:
        return '11:00 - 12:00'
    elif 12 <= h < 17:
        return '16:00 - 17:00'
    else:
        return None

# precip_mm_bin
def map_precip(mm):
    if mm <= 0:
        return 'Không mưa (0)'
    elif mm <= 2.5:
        return 'Mưa nhẹ (0 - 2.5)'
    else:
        return 'Mưa lớn (> 2.5)'

# wind_kph_bin
def map_wind(w):
    if w <= 10:
        return 'Yên lặng (< 11)'
    elif w <= 20:
        return 'Gió vừa (11 - 20)'
    else:
        return 'Gió mạnh (> 20)'

# vis_km_bin
def map_vis(v):
    if v <= 5:
        return 'Thấp (< 6)'
    elif v <= 10:
        return 'Trung bình (6 - 10)'
    else:
        return 'Cao (> 10)'

def transform_data(df):
    df['time'] = pd.to_datetime(df['time'])  # Chuyển time thành datetime
    df['delay_time'] = df['currentTravelTime'] - df['freeFlowTravelTime']  # Tính delay
    df['waiting'] = df['delay_time'].apply(map_waiting)
    df['hour'] = df['time'].dt.hour  # Trích giờ để lọc khung
    df['date'] = df['time'].dt.date

    df_filtered = df.dropna()  # Loại null nếu có
    df_filtered = df_filtered[df_filtered['delay_time'] >= 0]  # Loại delay âm
    df_filtered = df_filtered[df_filtered['roadClosure'] == False]  # Loại đường đóng

    df_filtered['period'] = df_filtered['hour'].apply(map_period)
    df_filtered['distance_bin'] = df_filtered['distance'].apply(map_distance)
    df_filtered['time_slot'] = df_filtered['hour'].apply(map_time_slot)
    df_filtered['precip_mm_bin'] = df_filtered['precip_mm'].apply(map_precip)
    df_filtered['wind_kph_bin'] = df_filtered['wind_kph'].apply(map_wind)
    df_filtered['vis_km_bin'] = df_filtered['vis_km'].apply(map_vis)

    lon_scale = (df["longitude"] - df["longitude"].min()) / \
                (df["longitude"].max() - df["longitude"].min())
    lat_scale = (df["latitude"] - df["latitude"].min()) / \
                (df["latitude"].max() - df["latitude"].min())
    lon_scale = round(lon_scale.astype(float), 2)
    lat_scale = round(lat_scale.astype(float), 2)
    df_filtered['x_img'] = 689 * (lon_scale) * 0.8 + 78
    df_filtered['y_img'] = 516 * (1 - lat_scale) * 0.8 + 78

    return df_filtered

