from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Register(db.Model):
    __tablename__ = 'users'

    sr_code = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)

class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(255), nullable=False)
    place = db.Column(db.String(255), nullable=False)
    photo = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Return(db.Model):
    __tablename__ = 'returns'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, nullable=False) 
    item_name = db.Column(db.String(255), nullable=False)
    place_found = db.Column(db.String(255), nullable=False)
    photo = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    claimed_by = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    timestamp_claimed = db.Column(db.DateTime, default=datetime.utcnow)