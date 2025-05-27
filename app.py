from flask import Flask
from flask_restx import Api
from config import Config
from extensions import db, bcrypt
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    # for production later
    # CORS(app, resources={r"/auth/*": {"origins": "https://your-frontend-domain.com"}})

    db.init_app(app)
    bcrypt.init_app(app)

    @app.route('/')
    def home():
        return "🚀 Mental Health API is running!"

    api = Api(
        app,
        version='1.0',
        title='Mental Health Assistant API',
        description='Documentation for PHQ-9 and GAD-7 Chatbot',
        doc='/docs'
    )

    from routes.auth_routes import auth_ns
    api.add_namespace(auth_ns, path='/auth')

    from routes.chat_routes import chat_ns
    api.add_namespace(chat_ns)

    from routes.chatbot_routes import chatbot_ns
    api.add_namespace(chatbot_ns)

    from routes.response_routes import response_ns
    api.add_namespace(response_ns)

    # Register Blueprints
    from routes.answer_routes import answer_bp

    app.register_blueprint(answer_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    print(f"📂 Using database path: {app.config['SQLALCHEMY_DATABASE_URI']}")
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True)
