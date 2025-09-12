from src.extensions import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.DateTime, nullable=True)
    time_estimate = db.Column(db.Integer, nullable=True)  # minutes
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # link to user

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "time_estimate": self.time_estimate,
            "user_id": self.user_id
        }
