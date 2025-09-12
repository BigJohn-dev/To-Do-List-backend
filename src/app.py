from flask import Flask

from src.config.config import DevelopmentConfig
from src.controllers.auth_controller import auth_bp
from src.extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)

    from src.controllers.task_controller import task_bp
    app.register_blueprint(task_bp, url_prefix="/tasks")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
