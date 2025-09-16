import os
import json
import psycopg2

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def connect_to_database():
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        port=os.environ.get("DB_PORT", 5432)
    )
    return conn

def create_database(conn):
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS traffic_information (
                    id SERIAL PRIMARY KEY,
                    description TEXT,
                    time TIMESTAMP,
                    distance NUMERIC,
                    frc TEXT,
                    currentSpeed NUMERIC,
                    freeFlowSpeed NUMERIC,
                    currentTravelTime NUMERIC,
                    freeFlowTravelTime NUMERIC,
                    confidence NUMERIC,
                    roadClosure BOOLEAN,
                    latitude NUMERIC,
                    longitude NUMERIC,
                    precip_mm NUMERIC,
                    vis_km NUMERIC,
                    wind_kph NUMERIC,
                    condition_text TEXT
                );
                CREATE TABLE IF NOT EXISTS traffic_information_transform (
                    id SERIAL PRIMARY KEY,
                    description TEXT,
                    distance NUMERIC,
                    time TIMESTAMP,
                    delay_time NUMERIC,
                    waiting TEXT,
                    hour INT,
                    period TEXT,
                    date DATE,
                    distance_bin TEXT,
                    time_slot TEXT,
                    condition_text TEXT,
                    precip_mm_bin TEXT,
                    wind_kph_bin TEXT,
                    vis_km_bin TEXT,
                    x_img NUMERIC,
                    y_img NUMERIC
                );
            """)
    conn.commit()
    cur.close()

def clean_database(conn):
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                DROP TABLE IF EXISTS traffic_information CASCADE;
                DROP TABLE IF EXISTS traffic_information_transform CASCADE;
            """)
    conn.commit()
    cur.close()
    create_database(conn)

def save_value(conn, data, type='raw'):
    if type == 'raw':
        insert_comment = """
                            INSERT INTO traffic_information (
                                description, time, distance, frc, currentSpeed, freeFlowSpeed,
                                currentTravelTime, freeFlowTravelTime, confidence, roadClosure,
                                latitude, longitude, precip_mm, vis_km, wind_kph, condition_text
                            ) VALUES (
                                %(description)s, %(time)s, %(distance)s, %(frc)s, %(currentSpeed)s, %(freeFlowSpeed)s,
                                %(currentTravelTime)s, %(freeFlowTravelTime)s, %(confidence)s, %(roadClosure)s,
                                %(latitude)s, %(longitude)s, %(precip_mm)s, %(vis_km)s, %(wind_kph)s, %(condition_text)s
                            );
                        """
    elif type == 'transform':
        insert_comment = """
                            INSERT INTO traffic_information_transform (
                                description, distance, time, delay_time, waiting, hour, period,
                                date, distance_bin, time_slot, condition_text,
                                precip_mm_bin, wind_kph_bin, vis_km_bin,
                                x_img, y_img
                            ) VALUES (
                                %(description)s, %(distance)s, %(time)s, %(delay_time)s, %(waiting)s, %(hour)s, %(period)s,
                                %(date)s, %(distance_bin)s, %(time_slot)s, %(condition_text)s,
                                %(precip_mm_bin)s, %(wind_kph_bin)s, %(vis_km_bin)s,
                                %(x_img)s, %(y_img)s
                            );
                        """
    else:
        return None

    with conn:
        with conn.cursor() as cur:
            cur.execute(insert_comment, data)

    conn.commit()
    cur.close()

def fetch_data(conn, type='raw'):
    select_comment = ""
    if type == 'raw':
        select_comment = """SELECT * FROM traffic_information;"""
    elif type == 'transform':
        select_comment = """SELECT * FROM traffic_information_transform;"""
    else:
        return None

    with conn:
        with conn.cursor() as cur:
            cur.execute(select_comment)
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            df = pd.DataFrame(rows, columns=columns)
    conn.commit()
    cur.close()
    return df
