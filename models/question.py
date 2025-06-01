from extensions import db

class Question(db.Model):
    __tablename__ = 'questions'

    question_id = db.Column(db.Integer, primary_key=True)
    question_type = db.Column(db.String(10), nullable=False)  # 'phq9' or 'gad7'
    question = db.Column(db.Text, nullable=False)