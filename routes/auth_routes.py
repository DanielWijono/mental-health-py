from flask import request
from flask_restx import Namespace, Resource, fields
from extensions import db, bcrypt, mail
from models.user import Users
from flask_mail import Message
import secrets

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
    
forgot_password_model = auth_ns.model('ForgotPassword', {
    'email': fields.String(required=True)
})

@auth_ns.route('/forgot-password')
class ForgotPassword(Resource):
    @auth_ns.expect(forgot_password_model)
    def post(self):
        data = request.get_json()
        email = data.get('email')

        user = Users.query.filter_by(email=email).first()
        if not user:
            return {'error': 'Email not found.'}, 404

        # generate token
        reset_token = secrets.token_urlsafe(32)

        # send email
        msg = Message('Reset Your Password',
                      sender='no-reply@mentalhealth.com',
                      recipients=[email])
        msg.body = f"Hi {user.name},\n\nClick this link to reset your password:\n\nhttps://your-frontend-url/reset-password/{reset_token}"
        mail.send(msg)

        return {'message': 'Reset link has been sent to your email.'}, 200
    
change_model = auth_ns.model("ChangePassword", {
    "email": fields.String(required=True),
    "new_password": fields.String(required=True)
})

@auth_ns.route('/change-password')
class ChangePassword(Resource):
    @auth_ns.expect(change_model)
    def post(self):
        data = request.get_json()
        email = data.get("email")
        new_password = data.get("new_password")

        if not email or not new_password:
            return {"error": "Email and new password are required."}, 400

        user = Users.query.filter_by(email=email).first()
        if not user:
            return {"error": "User not found."}, 404

        hashed_pw = bcrypt.generate_password_hash(str(new_password)).decode('utf-8')
        user.password_hash = hashed_pw
        db.session.commit()

        return {"message": "Password updated successfully."}, 200