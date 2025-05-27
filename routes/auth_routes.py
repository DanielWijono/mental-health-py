from flask import request
from flask_restx import Namespace, Resource, fields
from extensions import db, bcrypt
from models.user import Users

auth_ns = Namespace('auth', description='Authentication operations')

register_model = auth_ns.model('Register', {
    'name': fields.String(required=True, description='User name'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_model)
    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not all([name, email, password]):
            return {'message': 'Missing required fields.'}, 400

        if Users.query.filter_by(email=email).first():
            return {'message': 'Email already registered'}, 400

        hashed_pw = bcrypt.generate_password_hash(str(password)).decode('utf-8')
        new_user = Users(name=name.strip(), email=email.strip(), password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User registered successfully'}, 201

login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
})

@auth_ns.route('/login') 
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.doc(description="Login with email and password")
    def post(self):
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"error": "Email and password are required."}, 400

        user = Users.query.filter_by(email=email).first()

        if not user or not bcrypt.check_password_hash(user.password_hash, str(password)):
            return {"error": "Invalid email or password."}, 401

        return {
            "message": f"Welcome back, {user.name}!",
            "user_id": user.id
        }, 200