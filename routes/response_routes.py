from flask_restx import Namespace, Resource, fields
from flask import request
from extensions import db
from models.response import Responses
from models.user import Users        
from models.chat import Chat
from sqlalchemy.sql import func

import numpy as np
import joblib
import os

response_ns = Namespace('responses', description='User Responses Operations')

# 🔧 Swagger Model
combined_model = response_ns.model("ResponseWithChat", {
    "user_id": fields.Integer(required=True),
    "question_type": fields.String(required=True, enum=["phq9", "gad7", "general"]),
    "question_id": fields.Integer(required=True),
    "answer_value": fields.Integer(required=True, enum=[0, 1, 2, 3]),
    "message_type": fields.String(required=True, enum=["user", "bot"]),
    "message": fields.String(required=True)
})

@response_ns.route('/with-chat')
class SaveResponseWithChat(Resource):
    @response_ns.expect(combined_model)
    def post(self):
        """Save user response + chat in one request"""
        data = request.get_json()

        # Extract values
        user_id = data.get('user_id')
        question_type = data.get('question_type')
        question_id = data.get('question_id')
        answer_value = data.get('answer_value')
        message_type = data.get('message_type')  # 'user' or 'bot'
        message = data.get('message')

        # ✅ Validate required fields
        required = ['user_id', 'question_type', 'question_id', 'answer_value', 'message_type', 'message']
        missing = [field for field in required if field not in data or data[field] in [None, '']]
        if missing:
            return {'error': 'Missing fields: ' + ', '.join(missing)}, 400

        # ✅ Validate user
        user = Users.query.get(user_id)
        if not user:
            return {'error': f'User ID {user_id} not found'}, 404

        # ✅ Validate question_type
        valid_types = ['phq9', 'gad7', 'general']
        if question_type.lower() not in valid_types:
            return {'error': "question_type must be 'phq9', 'gad7', or 'general'"}, 400

        # ✅ Validate range and format
        if not (1 <= int(question_id) <= 17):
            return {'error': 'question_id must be between 1 and 17'}, 400
        if int(answer_value) not in [0, 1, 2, 3]:
            return {'error': 'answer_value must be 0, 1, 2, or 3'}, 400
        if message_type not in ['user', 'bot']:
            return {'error': "message_type must be 'user' or 'bot'"}, 400

        try:
            # 💾 Save response
            response = Responses(
                user_id=user_id,
                question_type=question_type.lower(),
                question_id=question_id,
                answer_value=answer_value
            )
            db.session.add(response)

            # 💾 Save chat
            chat = Chat(
                user_id=user_id,
                message_type=message_type,
                message=message
            )
            db.session.add(chat)

            db.session.commit()

            return {
                'message': 'Response and chat saved successfully',
                'response': {
                    'question_id': question_id,
                    'question_type': question_type,
                    'answer_value': answer_value
                },
                'chat': {
                    'message_id': chat.message_id,
                    'message_type': chat.message_type,
                    'message': chat.message,
                    'created_at': chat.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }, 201

        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500