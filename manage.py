from flask_pymongo import PyMongo

from src.app import create_app

# Initialize Flask app
app = create_app()

# Setup MongoDB
mongo = PyMongo(app)

with app.app_context():
    try:
        # Just test the connection
        mongo.cx.server_info()
        print("✅ MongoDB connected successfully!")
    except Exception as e:
        print("❌ MongoDB connection failed:", str(e))
