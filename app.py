from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
from exts import db
from models import Station, Station_Availability
from sqlalchemy.orm import aliased

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
    # Aliased to perform a self-join to get the latest record for each station
    station_alias = aliased(Station_Availability)
    subquery = db.session.query(
        station_alias.number,
        db.func.max(station_alias.last_update).label('latest_update')
    ).group_by(station_alias.number).subquery()

    latest_availability = db.session.query(Station,Station_Availability).\
        join(Station_Availability, Station.number == Station_Availability.number).\
        join(subquery,(Station_Availability.number == subquery.c.number) &
                        (Station_Availability.last_update == subquery.c.latest_update)).all()
    stations_list = [{
        'Number': station.number,
        'Address': station.address,
        'Bike_stands': station.bike_stands,
        'Available_bikes': availability.available_bikes,
        'Available_stands': availability.available_bike_stands,
        # 'last_update': availability.last_update
        'Status': 'Full' if availability.available_bikes == 0 else('Free' if availability.available_bikes / station.bike_stands >= 0.6 else 'Busy')
    } for station, availability in latest_availability]

    return jsonify(stations_list)





if __name__ == '__main__':
    app.run()
