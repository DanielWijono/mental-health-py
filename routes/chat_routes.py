from flask import request
from flask_restx import Namespace, Resource, fields
from models.chat import Chat
from models.user import Users
from extensions import db

chat_ns = Namespace('chats', description='Chat operations')

chat_model = chat_ns.model('Chat', {
    'user_id': fields.Integer(required=True, description='ID of the user'),
    'message_type': fields.String(required=True, description="Message type: 'user' or 'bot'", enum=['user', 'bot']),
    'message': fields.String(required=True, description='Chat message content')
})

chat_response = chat_ns.model('ChatResponse', {
    'message_id': fields.Integer,
    'user_id': fields.Integer,
    'message_type': fields.String,
    'message': fields.String,
    'created_at': fields.String
})

@chat_ns.route('')
class ChatCreate(Resource):
    @chat_ns.expect(chat_model)
    @chat_ns.response(201, 'Chat saved successfully', chat_response)
    @chat_ns.response(400, 'Missing or invalid fields')
    @chat_ns.response(409, 'User ID not found')
    def post(self):
        """Save a new chat message"""
        data = request.get_json()
        user_id = data.get('user_id')
        message_type = data.get('message_type')
        message = data.get('message')

        user = Users.query.filter_by(id=user_id).first()
        if not user:
            return {"error": f"User ID {user_id} not found."}, 409

        if not all([user_id, message_type, message]):
            return {"error": "Missing one or more required fields: user_id, message_type, message"}, 400

        if message_type not in ['user', 'bot']:
            return {"error": "message_type must be 'user' or 'bot'"}, 400

        new_chat = Chat(user_id=user_id, message_type=message_type, message=message)
        db.session.add(new_chat)
        db.session.commit()

        return {
            "message_id": new_chat.message_id,
            "user_id": new_chat.user_id,
            "message_type": new_chat.message_type,
            "message": new_chat.message,
            "created_at": new_chat.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }, 201
    
@chat_ns.route('/<int:user_id>')
@chat_ns.param('user_id', 'User ID')
class ChatHistory(Resource):
    @chat_ns.response(200, 'Success')
    @chat_ns.response(404, 'User not found')
    def get(self, user_id):
        """Retrieve all chat messages for a user"""
        user = Users.query.get(user_id)
        if not user:
            return {"error": f"User with ID {user_id} not found."}, 404

        chats = Chat.query.filter_by(user_id=user_id).order_by(Chat.created_at.asc()).all()

        return {
            "user_id": user_id,
            "chat_history": [
                {
                    "message_id": c.message_id,
                    "message_type": c.message_type,
                    "message": c.message,
                    "created_at": c.created_at.strftime("%Y-%m-%d %H:%M:%S")
                } for c in chats
            ]
        }, 200
