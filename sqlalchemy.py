from sqlalchemy import create_engine, Column, Integer, Float, String, MetaData
#from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('mysql+mysqlconnector://admin:group17SWE@subnet-0f43efe1ab41dd079:3306/mydatabase')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

#class Station(Base):
    

metadata = MetaData()
station = sqla.Table("station", metadata,
                     Column("address", String(256), nullable = False),
                     Column("banking", Integer),
                     Column("bike_stands", Integer),
                     Column("bonus", Integer),
                     Column("contract_name", String(256)),
                     Column("name", String(256)),
                     Column("number", Integer),
                     Column("position_lat", sqla.REAL),
                     Column("position_lng", sqla.REAL),
                     Column("status", String(256))
                    )

availability = sqla.Table("availability", metadata,
                          Column("available_bikes", Integer),
                          Column("avaialble_bike_stands", Integer),
                          Column("number", Integer),
                          Column("last_update", sqla.BigInteger)
                         )

try:
    station.drop(engine)
    availability.drop(engine)
except:
    pass

metadata.create_all(engine)


session.add(new_object1)
session.add(new_object2)

session.commit()
session.close()