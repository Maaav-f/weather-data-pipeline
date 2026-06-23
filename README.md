
# Wheather Data Pipeline  
Pipeline ETL automatizzata con Airflow per l'estrazione tramite API (OpenWeather) e lo storage di dati metereologici in tempo reale.
 

## Descrizione
Il DAG interroga l'API di OpenWeather ogni 10 minuti e quest'ultima risponde tramite un file .json. Il modello di risposta è contentuto nel file esempio.json.  
La normalizzazione dei dati avviene tramite Python e consiste nel selezionare soltanto alcuni parametri e convertire le relative unità di misura.
Lo storage avviene in un database MySQL in locale.

## Stack
Python, Apache Airflow, MySQL

## Struttura
├── dags/  
│   ├── dag_meteo.py         # DAG Airflow  
│   └── meteo_fun.py         # funzioni di estrazione e trasformazione  
├── .gitignore  
└── README.md  

## SetUp
1. Clona la repository
2. Crea un file .env con le seguenti variabili:

    *OpenWeather*  
    OPEN_WEATHER_API = your_openweather_api

    *MySQL*  
    MYSQL_HOST = your_mysql_host  
    MYSQL_USER = your_mysql_user  
    MYSQL_PSW = your_mysql_password  
    MYSQL_DATABASE = your_db_name  

4. Crea uno script .sql (anche direttamente su MySQL) contenente questi comandi:
    '''
    CREATE DATABASE your_db_name;

    CREATE USER 'your_mysql_user'@'%' IDENTIFIED BY 'your_mysql_password';  
    GRANT ALL PRIVILEGES ON your_db_name.* TO 'your_mysql_user'@'%';  

    FLUSH PRIVILEGES;  

    USE your_db_name;  

    CREATE TABLE dati_meteo(  
        id INT PRIMARY KEY AUTO_INCREMENT,  
        citta TEXT,  
        latitudine DOUBLE,  
        longitudine DOUBLE,  
        condizioni TEXT,  
        dettaglio_condizioni TEXT,  
        temperatura DOUBLE,  
        percepita DOUBLE,  
        data_ora DATETIME  
    );  
    '''
    
  Note: la gestione della tabella (creazione, truncation, ecc..) può essere automatizzata. Io ho deciso di crearla una sola    volta per comodità.

4. Crea un virtual environment. Io ho fatto tutto su VS Code, ma può essere fatto anche da terminale. Se scegliete di usare VSC, l'editor riconoscerà automaticamente un file requirements.txt e vi suggerirà di installare le librerie ivi contenute.
5. Avvia Airflow (con Docker o da terminale)
6. Avvia la DAG dall'interfaccia di Airflow
7. Enjoy!


