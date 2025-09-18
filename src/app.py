from flask import Flask
from flask_cors import CORS
from src.config.config import DevelopmentConfig
from src.controllers.auth_controller import auth_bp
from src.extensions import mongo

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    mongo.init_app(app)

    CORS(app, resources={r"/*": {"origins": "http://localhost:5174"}})

    from src.controllers.task_controller import task_bp
    app.register_blueprint(task_bp, url_prefix="/tasks")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
