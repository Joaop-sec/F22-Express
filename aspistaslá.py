import os
import pandas as pd
import sqlite3
import urllib.request

os.makedirs("data", exist_ok=True)

url_aeroportos = "https://davidmegginson.github.io/ourairports-data/airports.csv"
url_pistas = "https://davidmegginson.github.io/ourairports-data/runways.csv"

print("Baixando arquivos de aeroportos e pistas...")
urllib.request.urlretrieve(url_aeroportos, "airports.csv")
urllib.request.urlretrieve(url_pistas, "runways.csv")

df_aeroportos = pd.read_csv("airports.csv")
df_pistas = pd.read_csv("runways.csv")

conn = sqlite3.connect("data/bank.bd")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS aeroportos (
    id INTEGER PRIMARY KEY,
    ident TEXT UNIQUE,
    iata_code TEXT,
    type TEXT,
    name TEXT,
    municipality TEXT,
    iso_country TEXT,
    latitude REAL,
    longitude REAL,
    elevation_ft REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS pistas (
    id INTEGER PRIMARY KEY,
    airport_ident TEXT,
    ident TEXT,
    length_ft REAL,
    width_ft REAL,
    surface TEXT,
    closed INTEGER,
    le_lat REAL,
    le_lon REAL,
    le_heading REAL,
    he_lat REAL,
    he_lon REAL,
    he_heading REAL
)
""")

tipos_aceitos = {"large_airport", "medium_airport", "small_airport"}

for _, row in df_aeroportos.iterrows():
    if row["type"] not in tipos_aceitos:
        continue
    if pd.isna(row["latitude_deg"]) or pd.isna(row["longitude_deg"]):
        continue
    cursor.execute("""
    INSERT OR REPLACE INTO aeroportos (
        id, ident, iata_code, type, name, municipality, iso_country,
        latitude, longitude, elevation_ft
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row["id"],
        row["ident"],
        row["iata_code"] if pd.notna(row["iata_code"]) else None,
        row["type"],
        row["name"],
        row["municipality"] if pd.notna(row["municipality"]) else "",
        row["iso_country"] if pd.notna(row["iso_country"]) else "",
        row["latitude_deg"],
        row["longitude_deg"],
        row["elevation_ft"] if pd.notna(row["elevation_ft"]) else None
    ))

for _, row in df_pistas.iterrows():
    if pd.isna(row['le_latitude_deg']) or pd.isna(row['le_longitude_deg']):
        continue
    cursor.execute("""
    INSERT OR REPLACE INTO pistas (
        id, airport_ident, ident, length_ft, width_ft, surface, closed,
        le_lat, le_lon, le_heading, he_lat, he_lon, he_heading
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row['id'],
        row['airport_ident'],
        f"{row['le_ident']}/{row['he_ident']}" if pd.notna(row['le_ident']) and pd.notna(row['he_ident']) else None,
        row['length_ft'],
        row['width_ft'],
        row['surface'],
        row['closed'],
        row['le_latitude_deg'],
        row['le_longitude_deg'],
        row['le_heading_degT'],
        row['he_latitude_deg'],
        row['he_longitude_deg'],
        row['he_heading_degT']
    ))

conn.commit()
conn.close()
print("Importação de aeroportos e pistas concluída.")