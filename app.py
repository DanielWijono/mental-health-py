from flask import Flask
from flask_restx import Api
from config import Config
from extensions import db, bcrypt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    api = Api(
        app,
        version='1.0',
        title='Mental Health Assistant API',
        description='Documentation for PHQ-9 and GAD-7 Chatbot',
        doc='/docs'  # akses dokumentasi di /docs
    )

    from routes.auth_routes import auth_ns
    api.add_namespace(auth_ns, path='/auth')

    from routes.chat_routes import chat_ns
    api.add_namespace(chat_ns)

    from routes.chatbot_routes import chatbot_ns
    api.add_namespace(chatbot_ns)

    # Register Blueprints
    from routes.answer_routes import answer_bp
    from routes.response_routes import response_bp

    app.register_blueprint(answer_bp)
    app.register_blueprint(response_bp)

    @app.route('/')
    def home():
        return "🚀 Mental Health API is running!"

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    print(f"📂 Using database path: {app.config['SQLALCHEMY_DATABASE_URI']}")
    app.run(debug=True)
