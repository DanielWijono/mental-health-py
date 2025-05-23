
from flask import Blueprint, request, jsonify
from extensions import db
from models.response import Responses
from sqlalchemy.sql import func

response_bp = Blueprint('responses', __name__, url_prefix='/responses')

@response_bp.route('', methods=['POST'])
def save_response():
    data = request.get_json()
    user_id = data.get('user_id')
    question_type = data.get('question_type')  # 'phq9' or 'gad7'
    question_id = data.get('question_id')
    answer_value = data.get('answer_value')

    if not all([user_id, question_type, question_id, answer_value is not None]):
        return jsonify({'message': 'Missing required fields'}), 400

    response = Responses(
        user_id=user_id,
        question_type=question_type,
        question_id=question_id,
        answer_value=answer_value
    )
    db.session.add(response)
    db.session.commit()

    return jsonify({'message': 'Response saved successfully'}), 201

@response_bp.route('/summary/<int:user_id>', methods=['GET'])
def get_summary(user_id):
    # Ambil total skor untuk PHQ-9 dan GAD-7
    phq9_score = db.session.query(func.sum(Response.answer_value)).filter_by(user_id=user_id, question_type='phq9').scalar() or 0
    gad7_score = db.session.query(func.sum(Response.answer_value)).filter_by(user_id=user_id, question_type='gad7').scalar() or 0

    def interpret(score, tool):
        if tool == 'phq9':
            if score >= 20:
                return 'Severe depression'
            elif score >= 15:
                return 'Moderately severe'
            elif score >= 10:
                return 'Moderate'
            elif score >= 5:
                return 'Mild'
            else:
                return 'Minimal'
        if tool == 'gad7':
            if score >= 15:
                return 'Severe anxiety'
            elif score >= 10:
                return 'Moderate anxiety'
            elif score >= 5:
                return 'Mild anxiety'
            else:
                return 'Minimal anxiety'

    return jsonify({
        'user_id': user_id,
        'phq9_score': phq9_score,
        'phq9_interpretation': interpret(phq9_score, 'phq9'),
        'gad7_score': gad7_score,
        'gad7_interpretation': interpret(gad7_score, 'gad7')
    })
