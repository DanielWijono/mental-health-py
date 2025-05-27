from flask_restx import Namespace, Resource, fields
from flask import request
from chatbot.chatbot_flow import get_questionnaire_data, calculate_score, interpret_score
from models.user import Users
from models.question import Question
from models.answer_option import AnswerOption
from extensions import db

chatbot_ns = Namespace('chatbot', description='Chatbot operations')

# 🔧 Swagger Models
profile_update_model = chatbot_ns.model('ProfileUpdate', {
    'user_id': fields.Integer(
        required=True, 
        description='User ID',
        default=1),
    'age': fields.Integer(
        required=True, 
        description='Age (1–100)',
        default=25),
    'occupation': fields.String(
        required=True, 
        description='Occupation',
        default='programmer'),
    'gender': fields.String(
        required=True,
        description='Gender: male or female',
        default="male"
    )
})

score_input_model = chatbot_ns.model('ScoreInput', {
    'phq9_answers': fields.Raw(required=False, description='Dict of PHQ9 answers'),
    'gad7_answers': fields.Raw(required=False, description='Dict of GAD7 answers')
})

@chatbot_ns.route('/greeting')
class Greeting(Resource):
    def get(self):
        """Greet the user"""
        return {
            "message": "👋 Hi there! Welcome to the Mental Health Assistant Bot.\nPlease provide your name, age, gender(male, female), and occupation to get started."
        }, 200

@chatbot_ns.route('/profile')
class Profile(Resource):
    @chatbot_ns.expect(profile_update_model)
    def patch(self):
        """Update user age, occupation, and gender"""
        data = request.get_json()
        required_fields = ["user_id", "age", "occupation", "gender"]
        missing = [f for f in required_fields if f not in data or not str(data[f]).strip()]
        if missing:
            return {"error": "Missing field(s): " + ", ".join(missing)}, 400

        try:
            user_id = int(data["user_id"])
            age = int(data["age"])
            occupation = data["occupation"].strip()
            gender = data["gender"].strip().lower()

            if age < 1 or age > 100:
                return {"error": "Age must be between 1 and 100."}, 400
            if gender not in ["male", "female"]:
                return {"error": "Gender must be either 'male' or 'female'."}, 400

            user = Users.query.get(user_id)
            if not user:
                return {"error": "User not found."}, 404

            user.age = age
            user.occupation = occupation
            user.gender = gender
            db.session.commit()

            return {
                "message": f"Profile updated for {user.name}. Age: {age}, Occupation: {occupation}, Gender: {gender}."
            }, 200

        except ValueError:
            return {"error": "Age and user_id must be numbers."}, 400
        except Exception as e:
            return {"error": str(e)}, 500

@chatbot_ns.route('/score')
class Score(Resource):
    @chatbot_ns.expect(score_input_model)
    def post(self):
        """Calculate score & interpretation"""
        try:
            data = request.get_json()
            phq9_score = calculate_score(data.get('phq9_answers', {}))
            gad7_score = calculate_score(data.get('gad7_answers', {}))

            return {
                "phq9_score": phq9_score,
                "phq9_interpretation": interpret_score(phq9_score, 'phq9'),
                "gad7_score": gad7_score,
                "gad7_interpretation": interpret_score(gad7_score, 'gad7')
            }, 200
        except Exception as e:
            return {"error": str(e)}, 500


@chatbot_ns.route('/questions/<int:question_id>')
class QuestionByID(Resource):
    def get(self, question_id):
        """Get question and options by ID"""
        try:
            question = Question.query.filter_by(question_id=question_id).first()
            if not question:
                return {"error": f"Question ID {question_id} not found."}, 404

            options = AnswerOption.query.filter_by(type=question.question_type.upper()).order_by(AnswerOption.value).all()
            option_list = [{"label": o.label, "value": o.value} for o in options]

            return {
                "question_id": question.question_id,
                "question_type": question.question_type,
                "text": question.question,
                "options": option_list
            }, 200

        except Exception as e:
            return {"error": str(e)}, 500

@chatbot_ns.route('/questions')
class AllQuestions(Resource):
    def get(self):
        """Get all PHQ9 and GAD7 questions with options"""
        try:
            all_questions = Question.query.order_by(Question.question_id).all()
            result = []
            for q in all_questions:
                options = AnswerOption.query.filter_by(type=q.question_type.upper()).order_by(AnswerOption.value).all()
                option_list = [{"label": o.label, "value": o.value} for o in options]

                result.append({
                    "question_id": q.question_id,
                    "question_type": q.question_type,
                    "text": q.question,
                    "options": option_list
                })

            return result, 200

        except Exception as e:
            return {"error": str(e)}, 500
