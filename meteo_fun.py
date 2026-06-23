
import datetime
import os
import requests

import mysql.connector

from dotenv import load_dotenv, find_dotenv


load_dotenv()

API_KEY = os.getenv("OPEN_WEATHER_API")

mysql_conn_params = {
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PSW"),
    "database": os.getenv("MYSQL_DATABASE"),
    "host": os.getenv("MYSQL_HOST")
}

def connessione_estrazione(ti):
    
    CITY = "Milano"    # la città può essere modificata a proprio piacimento
    API_URL = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": CITY, "appid": API_KEY}

    # facciamo la richiesta all'API inserendo i parametri
    response = requests.get(API_URL, params) 

    # solleva un'eccezione (ferma lo script) se ci sono stati errori nella richiesta
    response.raise_for_status()

    # trasformo la risposta (json) in un oggetto python (dict in questo caso)
    diz_raw_data = response.json()
    
    # aggiungiamo il timestamp di ingestione (mi permette di risalire al momento esatto in cui ho scaricato i dati)
    #diz_raw_data["ingestion_ts"] = datetime.datetime.now(datetime.UTC).isoformat()
    
    # pusho diz_raw_data nel xcom
    ti.xcom_push(key="raw_data", value=diz_raw_data)

    print("Dati estratti correttamente")
    

def trasformazione(ti):
    raw_data = ti.xcom_pull(task_ids="connessione_estrazione", key="raw_data")

    clean_data = {
        "citta": raw_data["name"],
        "lat": raw_data["coord"]["lat"],
        "lon": raw_data["coord"]["lon"],
        "condizioni": raw_data["weather"][0]["main"],
        "dettaglio_condizioni": raw_data["weather"][0]["description"],
        "temperatura": round(raw_data["main"]["temp"] - 273.15, 2),
        "percepita": round(raw_data["main"]["feels_like"] - 273.15, 2),
        "data_ora": datetime.datetime.fromtimestamp(raw_data["dt"], tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    }

    ti.xcom_push(key="clean_data", value=clean_data)

    print(clean_data)
    print("Dati trasformati correttamente")


def carica_dati(ti):

    diz_clean = ti.xcom_pull(task_ids="trasformazione", key="clean_data")
    print("diz_clean:", diz_clean)
    
    # stabilisco connessione
    with mysql.connector.connect(**mysql_conn_params) as conn:
        with conn.cursor() as cur:
            query = """INSERT INTO dati_meteo (citta, latitudine, longitudine, condizioni, dettaglio_condizioni, temperatura, percepita, data_ora)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            
            cur.execute(query, tuple(diz_clean.values()))

        conn.commit()

    print("Dati inseriti correttamente")


    
