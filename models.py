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
    date_added = db.Column(db.DateTime, default=lambda: datetime.now())
    last_updated = db.Column(db.DateTime, onupdate=lambda: datetime.now())
    is_active = db.Column(db.Boolean, default=True)


class InventoryHistory(db.Model):
    __tablename__ = 'inventory_history'
    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)  # e.g., 'added', 'removed', 'updated'
    quantity_changed = db.Column(db.Integer, nullable=False)
    date_time = db.Column(db.DateTime, default=lambda: datetime.now())
    remarks = db.Column(db.String(255))

    inventory = db.relationship('Inventory', backref='history')
    user = db.relationship('User', backref='history')