import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# configure the database
database_url = os.environ.get("DATABASE_URL")
if not database_url or database_url.strip() == "":
    database_url = "sqlite:///furnitech.db"
elif database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Upload configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size - reduced for better performance

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# initialize the app with the extension
db.init_app(app)

# Import routes after app initialization
from routes import *

with app.app_context():
    # Make sure to import the models here or their tables won't be created
    import models
    db.create_all()
    
    # Create default admin user if doesn't exist
    from models import Admin
    from werkzeug.security import generate_password_hash
    
    if not Admin.query.first():
        admin = Admin(
            username='admin',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin)
        db.session.commit()
        print("Default admin created - username: admin, password: admin123")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
