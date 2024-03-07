from exts import db
class Station(db.Model):
    __tablename__ = 'station'
    address = db.Column(db.String(255))
    banking = db.Column(db.Integer)
    bike_stands = db.Column(db.Integer)
    bonus = db.Column(db.Integer)
    contract_name = db.Column(db.String(255))
    name = db.Column(db.String(255))
    number = db.Column(db.Integer,primary_key=True)
    position_lat = db.Column(db.Float)
    position_lng = db.Column(db.Float)
    status = db.Column(db.String(255))