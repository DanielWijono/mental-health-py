from flask import Blueprint, request, jsonify
from models.chat import Chat
from models.user import Users
from extensions import db

chat_bp = Blueprint('chats', __name__, url_prefix='/chats')

# ✅ Save a chat message
@chat_bp.route('', methods=['POST'])
def save_chat():
    data = request.get_json()

    user_id = data.get('user_id')
    message_type = data.get('message_type')
    message = data.get('message')

    # Validation
    if not all([user_id, message_type, message]):
        return jsonify({"error": "user_id, message_type, and message are required."}), 400

    new_chat = Chat(
        user_id=user_id,
        message_type=message_type,
        message=message
    )
    db.session.add(new_chat)
    db.session.commit()

    return jsonify({
        "message": "Chat saved successfully.",
        "chat_id": new_chat.message_id
    }), 201


# ✅ Retrieve all chats for a user

@chat_bp.route('/<int:user_id>', methods=['GET'])
def get_user_chats(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({
            "error": f"User with ID {user_id} not found."
        }), 404

    chats = Chat.query.filter_by(user_id=user_id).order_by(Chat.created_at.asc()).all()

    chat_history = [
        {
            "message_id": chat.message_id,
            "message_type": chat.message_type,
            "message": chat.message,
            "created_at": chat.created_at.strftime("%Y-%m-%d %H:%M:%S")
        } for chat in chats
    ]

    return jsonify({
        "user_id": user_id,
        "chat_history": chat_history
    }), 200

