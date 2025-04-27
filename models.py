from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer, unique=True, nullable=False)
    user_name = db.Column(db.String(100), nullable=False)


class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    serial_number = db.Column(db.String(100))
    quantity = db.Column(db.Integer, nullable=False, default=0)
    unit = db.Column(db.String(50))
    category = db.Column(db.String(100))
    location = db.Column(db.String(100))
    min_stock = db.Column(db.Integer)
    remarks = db.Column(db.String(255))
    date_added = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_updated = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, default=True)