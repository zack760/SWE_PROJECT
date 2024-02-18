import requests
import sqlalchemy as sqla
from sqlalchemy import declarative_base, sessionmaker
import datetime

api_key = "6850b2e0cc303dd8b429051d92aff4823fc9199b"
contract_name = "Dublin"

response = requests.get(f"https://api.jcdecaux.com/vls/v1/stations?contract={contract_name}&apiKey={api_key}")

if response.status_code == 200:
    #data = response.content.decode('utf-8')
    all_data = response.json()
else:
    print(response.status.code)


# from tabulate import tabulate

# table = []

# for station in data: 
#     ID = station["number"]
#     Name = station["name"]
#     Address = station["address"]
#     TotalStands = station["bike_stands"]
#     AvailableStands = station["available_bike_stands"]
#     AvailableBikes = station["available_bikes"]
#     Status = station["status"]
#     LastUpdate = station["last_update"]
#     table.append([ID, Name, Address, TotalStands, AvailableStands, AvailableBikes, Status, LastUpdate])

# headers = ["ID", "Name", "Address", "Total Stands", "Available Stands", "Available Bikes", "Status", "Last Update"]
# print(tabulate(table, headers=headers))


print(all_data)

test_data = [
    {'number': 42, 'address': 'Smithfield North', 'banking': False, 'bike_stands': 30, 'name': 'SMITHFIELD NORTH', 'position': {'lat': 53.349562, 'lng': -6.278198}, 'available_bike_stands': 0, 'available_bikes': 30, 'status': 'OPEN', 'last_update': 1708268584000},
    {'number': 30, 'address': 'Parnell Square North', 'position': {'lat': 53.3537415547453, 'lng': -6.26530144781526}}
]

engine = sqla.create_engine('mysql+mysqlconnector://admin:group17SWE@subnet-0f43efe1ab41dd079:3306/mydatabase')
Base = declarative_base()

class station(Base):
    __tablename__: "station"
    number = sqla.Column(sqla.Integer, primary_key=True)
    address = sqla.Column(sqla.String(128))
    banking = sqla.Column(sqla.Integer)
    bike_stands = sqla.Column(sqla.Integer)
    name = sqla.Column(sqla.String(128))
    position_lat = sqla.Column(sqla.Float)
    position_lng = sqla.Column(sqla.Float)

class availability(Base):
    __tablename__ = 'availability'
    number = sqla.Column(sqla.Integer, primary_key=True)
    last_update = sqla.Column(sqla.DateTime, primary_key=True)
    available_bikes = sqla.Column(sqla.Integer)
    available_bike_stands = sqla.Column(sqla.Integer)
    status = sqla.Column(sqla.String(256))

def insert_data(data):
    Session = sessionmaker(bind=engine)
    session = Session()

    for entry in data:
        station_entry = station(
            number = entry["number"],
            address = entry.get("address"),
            banking = 1 if entry.get("banking") else 0,
            bike_stands = entry.get("bike_stands"),
            name = entry.get("name"),
            position_lat = entry["position"]["lat"],
            position_lng = entry["position"]["lng"]
        )

        session.add(station_entry)

    for entry in data:
        if "last_update" in entry:
            availability_entry = availability(
                number = entry["number"],
                last_update = datetime.fromtimestamp(entry["last_update"]/1000),
                available_bikes = entry.get("available_bikes"),
                available_bike_stands = entry.get("available_bike_stands"),
                status = entry.get("status")
            ) 

            session.add(availability_entry)

    session.commit()
    session.close()

insert_data(test_data)