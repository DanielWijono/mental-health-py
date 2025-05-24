from flask_restx import Namespace, Resource, fields
from flask import request
from extensions import db
from models.response import Responses
from sqlalchemy.sql import func

response_ns = Namespace('responses', description='User Responses Operations')

# 🔧 Swagger Model
response_model = response_ns.model('Response', {
    'user_id': fields.Integer(required=True, description='User ID'),
    'question_type': fields.String(required=True, description='Question type (phq9/gad7)', enum=['phq9', 'gad7']),
    'question_id': fields.Integer(required=True, description='Question ID'),
    'answer_value': fields.Integer(required=True, description='Answer value (0-3)')
})

# ✅ Save Response
@response_ns.route('')
class SaveResponse(Resource):
    @response_ns.expect(response_model)
    def post(self):
        """Save user response for PHQ-9 or GAD-7"""
        data = request.get_json()
        user_id = data.get('user_id')
        question_type = data.get('question_type')
        question_id = data.get('question_id')
        answer_value = data.get('answer_value')

        if not all([user_id, question_type, question_id, answer_value is not None]):
            return {'message': 'Missing required fields'}, 400

        response = Responses(
            user_id=user_id,
            question_type=question_type,
            question_id=question_id,
            answer_value=answer_value
        )
        db.session.add(response)
        db.session.commit()

        return {'message': 'Response saved successfully'}, 201


# 📊 Summary for user_id
@response_ns.route('/summary/<int:user_id>')
class ResponseSummary(Resource):
    def get(self, user_id):
        """Get PHQ-9 and GAD-7 score summary for a user"""
        phq9_score = db.session.query(func.sum(Responses.answer_value)).filter_by(
            user_id=user_id, question_type='phq9').scalar() or 0
        gad7_score = db.session.query(func.sum(Responses.answer_value)).filter_by(
            user_id=user_id, question_type='gad7').scalar() or 0

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

        return {
            'user_id': user_id,
            'phq9_score': phq9_score,
            'phq9_interpretation': interpret(phq9_score, 'phq9'),
            'gad7_score': gad7_score,
            'gad7_interpretation': interpret(gad7_score, 'gad7')
        }, 200