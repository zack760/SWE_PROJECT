from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
from exts import db
from models import Station

# URI =  "ec2-13-48-194-24.eu-north-1.compute.amazonaws.com"
USER =  "admin"
PASSWORD = "comp30830"
# PORT ="3306"
DB =  "dbbikes"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{USER}:{PASSWORD}@localhost:3307/{DB}"

db.init_app(app)

@app.route('/')
def hello_world():  # put application's code here
   return render_template('template.html')

#try to connect to rds get scrap station data
@app.route('/stations')
def get_stations():
    stations = Station.query.all()
    station_list=[{
            'address': station.address,
            'banking': station.banking,
            'bike_stands': station.bike_stands,
            'bonus': station.bonus,
            'contract_name': station.contract_name,
            'name': station.name,
            'number': station.number,
            'position_lat': station.position_lat,
            'position_lng': station.position_lng,
            'status': station.status

    } for station in stations
    ]

    return jsonify(station_list)




if __name__ == '__main__':
    app.run()
