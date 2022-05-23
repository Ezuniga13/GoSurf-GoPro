import pyowm
import collections
from dotenv import load_dotenv 
from dotenv import find_dotenv
import os
import sqlite3
from datetime import datetime, timedelta, timezone

def get_forecast_api(lat, lon, API_KEY):
    own = pyowm.OWM(API_KEY)
    manager = own.weather_manager()
    sanfran_forecast_ = manager.one_call(lat, lon).forecast_hourly
    
    return sanfran_forecast_

def make_dict(sanfran_forecast_):
    sanfran_forecast = collections.defaultdict(list)
    for forecast in sanfran_forecast_:
        sanfran_forecast['reference_timestamp'].append(forecast.reference_time())
        sanfran_forecast['humidity'].append(forecast.humidity)
        sanfran_forecast['precipitation_proba'].append(forecast.precipitation_probability)
        sanfran_forecast['rain'].append(forecast.rain)
        sanfran_forecast['temperature'].append(forecast.temperature(unit='fahrenheit'))
        sanfran_forecast['wind'].append(forecast.wind())
        sanfran_forecast['status'].append(forecast.status)

    return sanfran_forecast


def create_table():
    try:
        conn = sqlite3.connect('weather.db')
        
    except sqlite3.OperationalError as e:
        raise e
    
    else:
        print('Connected!')
    curr = conn.cursor()
    create_table_command = ("""CREATE TABLE IF NOT EXISTS forecast(
        dt INTEGER NOT NULL,
        status TEXT NOT NULL,
        temp REAL NOT NULL
        )""")
    curr.execute(create_table_command)
    conn.commit()
    print('table created')

    return curr, conn

def insert_into_table(curr, conn, dt, status, temp):
    insert_into = (""" INSERT OR REPLACE INTO forecast
                            VALUES( ?, ?, ?);""")
    
    row_to_insert = (dt, status, temp)
    print(row_to_insert)
    curr.execute(insert_into, row_to_insert)
    conn.commit()
    print('row inserted')

def append_from_api_to_db(curr, conn, sanfran_forecast):
    """
        Parameters: Takes in a cursor and a dataframe that has new unique aliases.
        Returns: A printed Done statement in the terminal.
    """
    
    length_of_api = len(sanfran_forecast['status'])
    idx = 0
    while length_of_api > 0:
        dt = sanfran_forecast['reference_timestamp'][idx]
        dt = datetime.utcfromtimestamp(dt)
        status = sanfran_forecast['status'][idx]
        temp = sanfran_forecast['temperature'][idx]['temp']
        print(dt, status, temp)
        insert_into_table(curr, conn , dt, status, temp)
        length_of_api -= 1
        idx += 1
    
    conn.close()
    print('done')
    

if __name__ == '__main__':
    
    load_dotenv(dotenv_path=find_dotenv(), verbose=True)
    API_KEY = os.getenv('API_KEY')
    lat = 37.4919
    lon = -122.4992

    sanfran_forecast_ = get_forecast_api(lat, lon, API_KEY)
    sanfran_forecast = make_dict(sanfran_forecast_)
    curr, conn = create_table()
    append_from_api_to_db(curr,conn, sanfran_forecast)
    