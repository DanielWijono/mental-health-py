from flask import Flask
from config import Config
from extensions import db, bcrypt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    from routes.auth_routes import auth_bp
    from routes.answer_routes import answer_bp
    from routes.response_routes import response_bp
    from routes.chatbot_routes import chatbot_bp
    from routes.chat_routes import chat_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(answer_bp)
    app.register_blueprint(response_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(chat_bp)

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
