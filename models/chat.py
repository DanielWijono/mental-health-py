from extensions import db
from datetime import datetime

class Chat(db.Model):
    __tablename__ = 'chats'

    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    message_type = db.Column(db.String(20), nullable=False)  # e.g., 'user', 'bot'
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Optional relationship to User model
    user = db.relationship('Users', backref=db.backref('chats', lazy=True, cascade="all, delete"))

    def __repr__(self):
        return f"<Chat {self.message_id} by User {self.user_id}>"
