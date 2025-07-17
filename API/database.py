import os
import json
import psycopg2
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
            """)
    conn.commit()
    cur.close()

def clean_database(conn):
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                DROP TABLE IF EXISTS traffic_information CASCADE;
            """)
    conn.commit()
    cur.close()
    create_database(conn)

def save_value(conn, data):
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO traffic_information (
                    description, time, distance, frc, currentSpeed, freeFlowSpeed,
                    currentTravelTime, freeFlowTravelTime, confidence, roadClosure,
                    latitude, longitude, precip_mm, vis_km, wind_kph, condition_text
                ) VALUES (
                    %(description)s, %(time)s, %(distance)s, %(frc)s, %(currentSpeed)s, %(freeFlowSpeed)s,
                    %(currentTravelTime)s, %(freeFlowTravelTime)s, %(confidence)s, %(roadClosure)s,
                    %(latitude)s, %(longitude)s, %(precip_mm)s, %(vis_km)s, %(wind_kph)s, %(condition_text)s
                );
            """, data)
    conn.commit()
    cur.close()


