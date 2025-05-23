from extensions import db

class AnswerOption(db.Model):
    __tablename__ = 'answer_options'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False)  # e.g., 'PHQ9', 'GAD7'
    label = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Integer, nullable=False)
