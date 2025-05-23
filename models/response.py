from extensions import db
from datetime import datetime

class Responses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    question_type = db.Column(db.String(10), nullable=False)
    question_id = db.Column(db.Integer, nullable=False)
    answer_value = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


