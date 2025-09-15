from flask_sqlalchemy import SQLAlchemy
from src.app import create_app
from src.extensions import db

db = SQLAlchemy()

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully!")
