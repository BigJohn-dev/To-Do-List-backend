
from src.extensions import db
from datetime import datetime
from src.models.tag import task_tags, Tag

class Task(db.Model):
    __tablename__ = "task"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.DateTime, nullable=True)
    time_estimate = db.Column(db.Integer, nullable=True)

    tags = db.relationship("Tag", secondary=task_tags, backref="tasks")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "time_estimate": self.time_estimate,
            "tags": [tag.to_dict() for tag in self.tags]
        }
