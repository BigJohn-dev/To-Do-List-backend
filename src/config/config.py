import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "default-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tasks.db'))}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = "supersecretkey123"
    MONGO_URI = "mongodb://localhost:27017/todo_app"


class ProductionConfig(Config):
    DEBUG = False
