from datetime import datetime, timedelta, timezone
from pyowm.utils import timestamps, formatting
import pyowm
import collections
from dotenv import load_dotenv 
from dotenv import find_dotenv
import os
import sqlite3

def get_historic_api(lat,lon, API_KEY):
    """

    """
    yesterday_epoch = formatting.to_UNIXtime(timestamps.yesterday())
    two_days_ago_epoch = int((datetime.now() - timedelta(days=2)).replace(tzinfo=timezone.utc).timestamp())
    three_days_ago_epoch = int((datetime.now() - timedelta(days=3)).replace(tzinfo=timezone.utc).timestamp())
    
    owm = pyowm.OWM(API_KEY)
    manager = owm.weather_manager()
 
    one_call_yest = manager.one_call(lat, lon, dt=yesterday_epoch).forecast_hourly
    one_call_two = manager.one_call(lat, lon, dt=two_days_ago_epoch).forecast_hourly
    one_call_three = manager.one_call(lat, lon, dt=three_days_ago_epoch).forecast_hourly
   
    observed_weather_yest_ = one_call_yest
    observed_weather_two_ = one_call_two
    observed_weather_three_ = one_call_three
    
    return observed_weather_three_, observed_weather_two_, observed_weather_yest_

def make_dict(observed_weather_three_, observed_weather_two_, observed_weather_yest_):
    """ Returns three 
        Parameters:
        Returns:
    """
    sanfran_history =  collections.defaultdict(list)
    for weather in observed_weather_three_:
        sanfran_history['reference_timestamp'].append((weather.reference_time()))
        sanfran_history['status'].append(weather.status)
        sanfran_history['humidity'].append(weather.humidity)
        sanfran_history['rain'].append(weather.rain)
        sanfran_history['temperature'].append(weather.temperature(unit='fahrenheit'))
        sanfran_history['wind'].append(weather.wind())
        sanfran_history['pressure'].append(weather.pressure)

    for weather in observed_weather_two_:
        sanfran_history['reference_timestamp'].append((weather.reference_time()))
        sanfran_history['status'].append(weather.status)
        sanfran_history['humidity'].append(weather.humidity)
        sanfran_history['rain'].append(weather.rain)
        sanfran_history['temperature'].append(weather.temperature(unit='fahrenheit'))
        sanfran_history['wind'].append(weather.wind())
        sanfran_history['pressure'].append(weather.pressure)
    
    for weather in observed_weather_yest_:
        sanfran_history['reference_timestamp'].append((weather.reference_time()))
        sanfran_history['status'].append(weather.status)
        sanfran_history['humidity'].append(weather.humidity)
        sanfran_history['rain'].append(weather.rain)
        sanfran_history['temperature'].append(weather.temperature(unit='fahrenheit'))
        sanfran_history['wind'].append(weather.wind())
        sanfran_history['pressure'].append(weather.pressure)

    return sanfran_history


def create_table():
    try:
        conn = sqlite3.connect('weather.db')
        
    except sqlite3.OperationalError as e:
        raise e
    
    else:
        print('Connected!')
    curr = conn.cursor()
    create_table_command = ("""CREATE TABLE IF NOT EXISTS wind_time(
        dt TEXT NOT NULL,
        wind_speed REAL NOT NULL
        )""")
    curr.execute(create_table_command)
    conn.commit()
    print('table created')

    return curr, conn

def insert_into_table(curr, conn, dt, wind_speed):
    
    insert_into = (""" INSERT OR REPLACE INTO wind_time
                            VALUES( ?, ?);""")
    
    row_to_insert = (dt, wind_speed)
    curr.execute(insert_into, row_to_insert)
    conn.commit()
    print('row inserted')

def append_from_api_to_db(curr, conn, sanfran_history):
    """
        Parameters: Takes in a cursor and a dataframe that has new unique aliases.
        Returns: A printed Done statement in the terminal.
    """
    
    length_of_api = len(sanfran_history['wind'])
    idx = 0
    while length_of_api > 0:
        wind_speed = sanfran_history['wind'][idx]['speed']
        dt = sanfran_history['reference_timestamp'][idx]
        dt = datetime.utcfromtimestamp(dt)
        print(dt, wind_speed)
        insert_into_table(curr, conn , dt, wind_speed)
        length_of_api -= 1
        idx += 1
    
    conn.close()
    print('done')
    

if __name__ == '__main__':
    load_dotenv(dotenv_path=find_dotenv(), verbose=True)
    API_KEY = os.getenv('API_KEY')
    lat = 37.4919
    lon = -122.4992
    observed_weather_three_, observed_weather_two_, observed_weather_yest_  = get_historic_api(lat, lon, API_KEY)
    sanfran_history = make_dict(observed_weather_three_, observed_weather_two_, observed_weather_yest_)
    curr, conn = create_table()
    append_from_api_to_db(curr,conn, sanfran_history)
    
    