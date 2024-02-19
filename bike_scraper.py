import requests
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime
import datetime
import time
import os

URI = os.getenv("DB_URI", "dbbikes.cf6ecqu48kpy.eu-north-1.rds.amazonaws.com")
USER = os.getenv("DB_USER", "admin")
PASSWORD = os.getenv("DB_PASSWORD", "comp30830")
PORT = os.getenv("DB_PORT", "3306")
DB = os.getenv("DB_NAME", "dbbikes")
APIKEY = os.getenv("JCDECAUX_APIKEY", "6850b2e0cc303dd8b429051d92aff4823fc9199b")
NAME = "Dublin"
STATIONS = "https://api.jcdecaux.com/vls/v1/stations"

# SQLAlchemy engine for MySQL connection
engine = create_engine(f'mysql://{USER}:{PASSWORD}@{URI}:{PORT}/{DB}', echo=True)

# Metadata instance for SQLAlchemy
metadata = MetaData()

# Station table definition
station = Table(
    'station', metadata,
    Column('address', String(256), nullable=False),
    Column('banking', Integer),
    Column('bike_stands', Integer),
    Column('bonus', Integer),
    Column('contract_name', String(256)),
    Column('name', String(256)),
    Column('number', Integer, primary_key=True),
    Column('position_lat', Float),
    Column('position_lng', Float),
    Column('status', String(256))
)

# Availability table definition
availability = Table(
    'availability', metadata,
    Column('number', Integer, primary_key=True),
    Column('available_bikes', Integer),
    Column('available_stands', Integer),
    Column('last_update', DateTime),
)

metadata.create_all(engine)

def fetch_and_insert_data():
    while True:
        try:
            response = requests.get(STATIONS, params={"contract": NAME, "apiKey": APIKEY})
            
            if response.status_code == 200:
                stations_data = response.json()
                
                with engine.connect() as connection:
                    
                    # Prepare data for bulk insert to improve performance
                    station_inserts = [{
                        'address': station_data['address'],
                        'banking': station_data['banking'],
                        'bike_stands': station_data['bike_stands'],
                        'bonus': station_data['bonus'],
                        'contract_name': station_data['contract_name'],
                        'name': station_data['name'],
                        'number': station_data['number'],
                        'position_lat': station_data['position']['lat'],
                        'position_lng': station_data['position']['lng'],
                        'status': station_data['status']
                    } for station_data in stations_data]
                    
                    availability_inserts = [{
                        'number': station_data['number'],
                        'available_bikes': station_data['available_bikes'],
                        'available_stands': station_data['available_stands'],
                        'last_update': datetime.datetime.fromtimestamp(station_data['last_update'] / 1e3)
                    } for station_data in stations_data]
                    
                    # Execute bulk inserts
                    connection.execute(station.insert(), station_inserts)
                    connection.execute(availability.insert(), availability_inserts)
            else:
                print(f"Failed to fetch data: {response.status_code}")
                
            time.sleep(5*60)  # Wait for 5 minutes before fetching new data
            
        except Exception as e:
            print(f"An error occurred: {e}")

# Run the function
if __name__ == '__main__':
    fetch_and_insert_data()