import pyowm
from dotenv import load_dotenv 
from dotenv import find_dotenv
import os
import sqlite3
from datetime import datetime, timedelta, timezone



def get_current_api(lat, lon, API_KEY):
    own = pyowm.OWM(API_KEY)
    manager = own.weather_manager()
    sanfran_current_ = manager.one_call(lat, lon)

    return sanfran_current_.current

def make_dict(sanfran_current_):
    sanfran_current = {}
    sanfran_current['reference_timestamp'] = sanfran_current_.reference_time()
    sanfran_current['status'] = sanfran_current_.status
    sanfran_current['humidity'] = sanfran_current_.humidity
    sanfran_current['rain'] = sanfran_current_.rain
    sanfran_current['current_temp'] = sanfran_current_.temperature(unit='fahrenheit')
    sanfran_current['wind_speed'] = sanfran_current_.wind()

    return sanfran_current


def create_table():
    try:
        conn = sqlite3.connect('weather.db')
        
    except sqlite3.OperationalError as e:
        raise e
    
    else:
        print('Connected!')
    curr = conn.cursor()
    create_table_command = ("""CREATE TABLE IF NOT EXISTS current_temperature(
        dt INTEGER NOT NULL,
        status TEXT NOT NULL,
        temp REAL NOT NULL
        )""")
    curr.execute(create_table_command)
    conn.commit()
    print('table created')

    return curr, conn

def insert_into_table(curr, conn, dt, status , temp):
    
    insert_into = (""" INSERT OR REPLACE INTO current_temperature
                            VALUES( ?, ?, ?);""")
    
    row_to_insert = (dt, status, temp)
    print(row_to_insert)
    curr.execute(insert_into, row_to_insert)
    conn.commit()
    print('row inserted')

def append_from_api_to_db(curr, conn, sanfran_current):
    """
        Parameters: Takes in a cursor and a dataframe that has new unique aliases.
        Returns: A printed Done statement in the terminal.
    """
    dt = sanfran_current['reference_timestamp']
    dt = datetime.utcfromtimestamp(dt)
    status = sanfran_current['status']
    temp = sanfran_current['current_temp']['temp']
    
    insert_into_table(curr, conn , dt, status,temp)
    
    print(dt, status, temp)
    conn.close()
    print('done')

if __name__ == '__main__':
    load_dotenv(dotenv_path=find_dotenv(), verbose=True)
    API_KEY = os.getenv('API_KEY')
    lat = 37.4919
    lon = -122.4992
    sanfran_current_ = get_current_api(lat,lon, API_KEY)
    sanfran_current = make_dict(sanfran_current_)
    print(sanfran_current)
    curr, conn = create_table()
    append_from_api_to_db(curr,conn, sanfran_current)
    
    
    

        
    