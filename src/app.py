from flask import Flask

from src.config.config import DevelopmentConfig
from src.extensions import db
from src.reminders.scheduler import init_scheduler


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)

    from src.controllers.task_controller import task_bp
    app.register_blueprint(task_bp, url_prefix="/tasks")

    with app.app_context():
        init_scheduler(app)

    return app



if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
