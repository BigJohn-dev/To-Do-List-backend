import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "default-secret-key")

class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = "supersecretkey123"
    MONGO_URI = "mongodb://localhost:27017/todo_app"


class ProductionConfig(Config):
    DEBUG = False
