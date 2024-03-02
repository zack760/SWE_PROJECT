import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
import json 
import os

URI = os.getenv("DB_URI", "dbbikes.cf6ecqu48kpy.eu-north-1.rds.amazonaws.com")
USER = os.getenv("DB_USER", "admin")
PASSWORD = os.getenv("DB_PASSWORD", "comp30830")
PORT = os.getenv("DB_PORT", "3306")
DB = os.getenv("DB_NAME", "dbbikes")

#engine = create_engine(f'mysql://{USER}:{PASSWORD}@{URI}:{PORT}/{DB}', echo=True, pool_pre_ping=True)

connection_string = (f"mysql+mysqlconnector://{USER}:{PASSWORD}@{URI}/{DB}")
engine = create_engine(connection_string)

query = f"SELECT * FROM station"
df = pd.read_sql(query, engine)
data_json = df.to_dict(orient="records")
json_file_path = "data.json"

with open(json_file_path, "w") as json_file:
    json.dump(data_json, json_file)

print("Data has successfully been added to the json file")
