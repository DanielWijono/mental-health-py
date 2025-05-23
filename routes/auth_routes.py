from flask import Blueprint, request, jsonify
from extensions import db, bcrypt
from models.user import Users

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # Check for missing fields
    missing = [field for field in ['name', 'email', 'password'] if not data.get(field)]
    if missing:
        return jsonify({'message': f"Missing field(s): {', '.join(missing)}"}), 400

    # Check if email already exists
    if Users.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered'}), 400

    try:
        # Force password to string (handles int, float, etc.)
        password = str(password)

        # Hash and save user
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = Users(name=name.strip(), email=email.strip(), password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201

    except Exception as e:
        return jsonify({'message': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    user = Users.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Invalid email or password."}), 401

    if not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password."}), 401

    return jsonify({
        "message": f"Welcome back, {user.name}!",
        "user_id": user.id
    }), 200