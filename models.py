from app import db
from datetime import datetime
from flask_login import UserMixin


class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)


class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(50), nullable=False)  # 'home', 'about'
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(20), nullable=False)  # 'office' or 'home'
    image_path = db.Column(db.String(200))
    order_index = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    service_interest = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class SiteSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    logo_path = db.Column(db.String(200))
    whatsapp_number = db.Column(db.String(20), default="+91XXXXXXXXXX")
    phone_number = db.Column(db.String(20), default="+91 9702030763")
    email = db.Column(db.String(100), default="admin@mtsfurnitech.com")
    address = db.Column(db.Text, default="R.No.67, 1st floor, LBS Nagar, korba mithaghar, wadala East Mumbai 700037")
    company_name = db.Column(db.String(100), default="MTS Furnitech")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
