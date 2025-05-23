import sqlite3
from models.question import Question
from models.answer_option import AnswerOption

def get_questionnaire_data():
    phq9 = Question.query.filter_by(question_type='phq9').order_by(Question.question_id).all()
    gad7 = Question.query.filter_by(question_type='gad7').order_by(Question.question_id).all()

    phq9_questions = [{"id": q.question_id, "text": q.question} for q in phq9]
    gad7_questions = [{"id": q.question_id, "text": q.question} for q in gad7]

    # You can keep answer_options logic as is
    phq9_opts = AnswerOption.query.filter_by(type='PHQ9').order_by(AnswerOption.value).all()
    gad7_opts = AnswerOption.query.filter_by(type='GAD7').order_by(AnswerOption.value).all()

    phq9_options = [{"label": opt.label, "value": opt.value} for opt in phq9_opts]
    gad7_options = [{"label": opt.label, "value": opt.value} for opt in gad7_opts]

    return {
        "phq9": phq9_questions,
        "gad7": gad7_questions,
        "phq9_options": phq9_options,
        "gad7_options": gad7_options
    }

def validate_user_profile(name, age, gender, occupation):
    """Validate and format user profile inputs."""
    if not name or not occupation:
        raise ValueError("Name and occupation cannot be empty.")

    if not age.isdigit() or not (1 <= int(age) <= 100):
        raise ValueError("Age must be a number between 1 and 100.")

    gender = gender.lower()
    if gender not in ["male", "female"]:
        raise ValueError("Gender must be either 'male' or 'female'.")

    return {
        "name": name.strip(),
        "age": int(age),
        "gender": gender,
        "occupation": occupation.strip()
    }

def calculate_score(responses):
    """
    Calculate total score from a dictionary of responses.
    Example input: {1: 2, 2: 3, 3: 1}
    """
    return sum(responses.values())

def interpret_score(score, scale):
    """
    Interpret PHQ-9 or GAD-7 score.
    """
    if scale.lower() == 'phq9':
        if score >= 20:
            return 'Severe depression'
        elif score >= 15:
            return 'Moderately severe depression'
        elif score >= 10:
            return 'Moderate depression'
        elif score >= 5:
            return 'Mild depression'
        else:
            return 'Minimal depression'

    elif scale.lower() == 'gad7':
        if score >= 15:
            return 'Severe anxiety'
        elif score >= 10:
            return 'Moderate anxiety'
        elif score >= 5:
            return 'Mild anxiety'
        else:
            return 'Minimal anxiety'

    return "Unknown scale"

