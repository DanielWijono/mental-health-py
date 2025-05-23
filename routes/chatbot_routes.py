from flask import Blueprint, jsonify, request
from chatbot.chatbot_flow import (
    get_questionnaire_data,
    calculate_score,
    interpret_score
)
from models.user import Users
from models.question import Question
from models.answer_option import AnswerOption
from extensions import db

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/chatbot')

@chatbot_bp.route('/greeting', methods=['GET'])
def greeting():
    return jsonify({
        "message": "👋 Hi there! Welcome to the Mental Health Assistant Bot.\nPlease provide your name, age, gender(male, female), and occupation to get started."
    }), 200

@chatbot_bp.route('/profile', methods=['PATCH'])
def update_profile():
    data = request.get_json()
    required_fields = ["user_id", "age", "occupation"]

    missing_fields = [field for field in required_fields if field not in data or not str(data[field]).strip()]
    if missing_fields:
        return jsonify({"error": "Missing required field(s): " + ", ".join(missing_fields)}), 400

    try:
        user_id = int(data["user_id"])
        age = int(data["age"])
        occupation = data["occupation"].strip()

        if age < 1 or age > 100:
            return jsonify({"error": "Age must be between 1 and 100."}), 400

        user = Users.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found."}), 404

        user.age = age
        user.occupation = occupation
        db.session.commit()

        return jsonify({
            "message": f"✅ Profile updated for {user.name}. Age: {age}, Occupation: {occupation}."
        }), 200

    except ValueError:
        return jsonify({"error": "Age and user_id must be numbers."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route('/score', methods=['POST'])
def score():
    data = request.get_json()

    try:
        phq9_score = calculate_score(data.get('phq9_answers', {}))
        gad7_score = calculate_score(data.get('gad7_answers', {}))

        return jsonify({
            "phq9_score": phq9_score,
            "phq9_interpretation": interpret_score(phq9_score, 'phq9'),
            "gad7_score": gad7_score,
            "gad7_interpretation": interpret_score(gad7_score, 'gad7')
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route('/questions/<int:question_id>', methods=['GET'])
def get_question_by_id(question_id):
    try:
        question = Question.query.filter_by(question_id=question_id).first()
        if not question:
            return jsonify({"error": f"Question ID {question_id} not found."}), 404

        # Get related answer options based on question_type
        options = AnswerOption.query.filter_by(type=question.question_type.upper()).order_by(AnswerOption.value).all()
        option_list = [{"label": opt.label, "value": opt.value} for opt in options]

        return jsonify({
            "question_id": question.question_id,
            "question_type": question.question_type,
            "text": question.question,
            "options": option_list
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@chatbot_bp.route('/questions', methods=['GET'])
def get_all_questions():
    try:
        all_questions = Question.query.order_by(Question.question_id).all()

        result = []
        for q in all_questions:
            options = AnswerOption.query.filter_by(type=q.question_type.upper()).order_by(AnswerOption.value).all()
            option_list = [{"label": opt.label, "value": opt.value} for opt in options]

            result.append({
                "question_id": q.question_id,
                "question_type": q.question_type,
                "text": q.question,
                "options": option_list
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
