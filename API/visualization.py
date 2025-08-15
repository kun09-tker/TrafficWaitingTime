import cv2
import database
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

from matplotlib.colors import LinearSegmentedColormap
from transform_traffic import transform_data, get_all_weather

@st.cache_data
def load_data():
    conn = database.connect_to_database()
    df = database.fetch_data(conn)
    df = transform_data(df)
    conn.close()
    return df

def daily_slider(dates):
    date_index = st.sidebar.select_slider(
        'Chọn ngày để xem dữ liệu:',
        options=dates,
        value=dates[0]  # Giá trị mặc định là ngày đầu tiên
    )  # Hiển thị ngày thay vì chỉ số
    return date_index

@st.cache_data
def vi_describe_data(df):
    st.subheader(f'Thống kê mô tả cho ngày {selected_date.strftime("%Y-%m-%d")}')
    st.dataframe(df.describe())

@st.cache_data
def vi_delay_time_by_time(df, df_to_date):
    st.markdown("#### Theo khung giờ 🕕")

    fig, ax = plt.subplots(figsize=(16, 10))
    plt.subplot(1, 2, 1)
    sns.boxplot(x='time_slot', y='delay_time', hue='description', data=df)
    plt.title('Biểu đồ boxplot cho thời gian chờ theo khung giờ')
    plt.xlabel('Khung giờ (giờ)')
    plt.ylabel('Thời gian chờ (giây)')
    plt.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=2)
    plt.subplot(1, 2, 2)
    grouped = (
        df_to_date.groupby(['date', 'time_slot', 'description'])['delay_time']
        .mean()
        .reset_index()
    )
    markers = ['o', 's', 'D']
    for (cat, mark) in zip(grouped['description'].unique(), markers):
        sub_df = grouped[grouped['description'] == cat]
        sns.lineplot(data=sub_df,
                    x='date',
                    y='delay_time',
                    style='description',
                    hue='time_slot',
                    marker=mark,
                    dashes=False)
    plt.title('Theo dõi trung bình thời gian chờ theo khung giờ qua từng ngày')
    plt.xlabel('Ngày')
    plt.ylabel('Thời gian chờ trung bình (giây)')
    plt.xticks(rotation=75)
    plt.legend(bbox_to_anchor=(0.5, -0.2), loc='upper center', ncol=2)
    ax.set_axis_off()
    plt.tight_layout()
    st.pyplot(fig)

@st.cache_data
def vi_delay_time_by_weather(df, df_to_date, args = None):
    st.markdown("#### Theo thời tiết 🌦️")
    markers = ['o', 's', 'D']

    fig, ax = plt.subplots(figsize=(16, 10))
    plt.subplot(1, 2, 1)
    sns.boxplot(x='precip_mm_bin', y='delay_time', hue='description', data=df)
    plt.title('Biểu đồ boxplot cho thời gian chờ theo lượng mưa')
    plt.xlabel('Lượng mưa (mm)')
    plt.ylabel('Thời gian chờ (giây)')
    plt.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=2)
    plt.subplot(1, 2, 2)
    grouped = (
        df_to_date.groupby(['date', 'precip_mm_bin', 'description'])['delay_time']
        .mean()
        .reset_index()
    )
    for (cat, mark) in zip(grouped['description'].unique(), markers):
        sub_df = grouped[grouped['description'] == cat]
        sns.lineplot(data=sub_df,
                    x='date',
                    y='delay_time',
                    style='description',
                    hue='precip_mm_bin',
                    marker=mark,
                    dashes=False)
    plt.title('Theo dõi trung bình thời gian chờ theo lượng mưa qua từng ngày')
    plt.xlabel('Ngày')
    plt.ylabel('Thời gian chờ trung bình (giây)')
    plt.xticks(rotation=75)
    plt.legend(bbox_to_anchor=(0.5, -0.2), loc='upper center', ncol=2)
    ax.set_axis_off()
    plt.tight_layout()
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(16, 10))
    plt.subplot(1, 2, 1)
    sns.boxplot(x='wind_kph_bin', y='delay_time', hue='description', data=df)
    plt.title('Biểu đồ boxplot cho thời gian chờ theo sức gió')
    plt.xlabel('Sức gió (km/h)')
    plt.ylabel('Thời gian chờ (giây)')
    plt.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=2)
    plt.subplot(1, 2, 2)
    grouped = (
        df_to_date.groupby(['date', 'wind_kph_bin', 'description'])['delay_time']
        .mean()
        .reset_index()
    )
    for (cat, mark) in zip(grouped['description'].unique(), markers):
        sub_df = grouped[grouped['description'] == cat]
        sns.lineplot(data=sub_df,
                    x='date',
                    y='delay_time',
                    style='description',
                    hue='wind_kph_bin',
                    marker=mark,
                    dashes=False)
    plt.title('Theo dõi trung bình thời gian chờ theo sức gió qua từng ngày')
    plt.xlabel('Ngày')
    plt.ylabel('Thời gian chờ trung bình (giây)')
    plt.xticks(rotation=75)
    plt.legend(bbox_to_anchor=(0.5, -0.2), loc='upper center', ncol=2)
    ax.set_axis_off()
    plt.tight_layout()
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(16, 10))
    plt.subplot(1, 2, 1)
    sns.boxplot(x='vis_km_bin', y='delay_time', hue='description', data=df)
    plt.title('Biểu đồ boxplot cho thời gian chờ theo tầm nhìn')
    plt.xlabel('Tầm nhìn (km)')
    plt.ylabel('Thời gian chờ (giây)')
    plt.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=2)
    plt.subplot(1, 2, 2)
    grouped = (
        df_to_date.groupby(['date', 'vis_km_bin', 'description'])['delay_time']
        .mean()
        .reset_index()
    )
    for (cat, mark) in zip(grouped['description'].unique(), markers):
        sub_df = grouped[grouped['description'] == cat]
        sns.lineplot(data=sub_df,
                    x='date',
                    y='delay_time',
                    style='description',
                    hue='vis_km_bin',
                    marker=mark,
                    dashes=False)
    plt.title('Theo dõi trung bình thời gian chờ theo tầm nhìn qua từng ngày')
    plt.xlabel('Ngày')
    plt.ylabel('Thời gian chờ trung bình (giây)')
    plt.xticks(rotation=75)
    plt.legend(bbox_to_anchor=(0.5, -0.2), loc='upper center', ncol=2)
    ax.set_axis_off()
    plt.tight_layout()
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(y='condition_text_vn', x='delay_time', hue='description', data=df, order=args['category_weather'])
    ax.set_title('Biểu đồ thời gian chờ trung bình theo tình trạng của thời tiết')
    ax.set_ylabel('Tình trạng thời tiết')
    ax.set_xlabel('Thời gian chờ (s)')
    ax.set_xlim(0, args['max_delay_time'])
    plt.xticks(rotation=45)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(fig)

@st.cache_data
def vi_heatmap_delay_time_by_weather(df):
    from_date = df['date'].min()
    to_date = df['date'].max()
    fig, ax = plt.subplots(figsize=(10, 6))
    corr = df[['delay_time', 'precip_mm', 'vis_km', 'wind_kph']].corr()
    corr.index = ['Thời gian chờ', 'Lượng mưa (mm)', 'Tầm nhìn (km)', 'Gió (km/h)']
    corr.columns = ['Thời gian chờ', 'Lượng mưa (mm)', 'Tầm nhìn (km)', 'Gió (km/h)']
    sns.heatmap(corr, annot=True)
    ax.set_title('Biểu đồ tương quan giữa thời gian chờ, lượng mưa, tầm nhìn và sức gió\n' \
                 f'Từ {from_date} đến {to_date}')
    plt.tight_layout()
    st.pyplot(fig)

@st.cache_data
def vi_delay_time_by_distance(df):
    st.markdown("#### Theo khoảng cách đến điểm đến 🛣️")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x='distance', y='delay_time', hue='description', style='time_slot', size='time_slot', sizes=(50, 50))
    ax.set_title('Biểu đồ thời gian chờ theo khoảng cách đến điểm đến')
    ax.set_xlabel('Khoảng cách đến điểm đến (m)')
    ax.set_ylabel('Thời gian chờ (s)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(fig)

@st.cache_data
def vi_map(df):
    from_date = df['date'].min()
    to_date = df['date'].max()

    x_coords = df['x_img'].astype(int)
    y_coords = df['y_img'].astype(int)
    weights = (df['delay_time'] - df['delay_time'].min()) \
               / (df['delay_time'].max() - df['delay_time'].min())

    image = cv2.imread("API/image/map.png")
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    colors = ["lightblue", "yellow", "red"]
    cmap = LinearSegmentedColormap.from_list("green_to_red", colors)
    heatmap_gray = np.zeros_like(image_rgb[:, :, 0], dtype=np.float32)

    for x, y, w in zip(x_coords, y_coords, weights.astype(float)):
        heatmap_gray[y, x] += w * 255

    heatmap_gray = cv2.GaussianBlur(heatmap_gray, (105, 105), 0)
    heatmap_normalized = heatmap_gray / heatmap_gray.max() if heatmap_gray.max() > 0 else heatmap_gray
    heatmap_colored = (cmap(heatmap_normalized)[:, :, :3] * 255).astype(np.uint8)
    kernel = np.array([[0, -1, 0],
                    [-1, 5, -1],
                    [0, -1, 0]])
    sharpened_image = cv2.filter2D(image_rgb, -1, kernel)

    alpha = 0.5
    blended_image = cv2.addWeighted(sharpened_image, 1 - alpha, heatmap_colored, alpha, 0)

    fig, ax = plt.subplots(figsize=(10, 10))
    plt.imshow(blended_image)
    ax.set_title('Biểu đồ mật độ kẹt xe trên các tuyến đường\n' \
                 f'Từ {from_date} đến {to_date}')
    plt.axis('off')
    st.pyplot(fig)

if __name__ == "__main__":
    df = load_data()
    st.title('Traffic Data Visualization')
    unique_dates = sorted(df['date'].unique())

    if len(unique_dates) > 0:
        selected_date = daily_slider(unique_dates)
    else:
        st.warning('Không có ngày nào trong dữ liệu.')
        st.stop()

    df_date = df[df['date'] == selected_date]
    df_to_date = df[df['date'] <= selected_date]
    if df_date.empty:
        st.warning(f'Không có dữ liệu cho ngày {selected_date.strftime("%Y-%m-%d")}.')
    else:
        vi_describe_data(df_date)
        vi_map(df_to_date)

        st.subheader('Thời gian chờ🚦khi tham gia giao thông 🚗💨:')
        vi_delay_time_by_time(df_date, df_to_date)

        vi_delay_time_by_distance(df_to_date)

        category_weather, max_delay_time = get_all_weather(df)
        args = {
            'category_weather': category_weather,
            'max_delay_time': max_delay_time
        }
        vi_delay_time_by_weather(df_date, df_to_date, args)
        vi_heatmap_delay_time_by_weather(df_to_date)
