from flask import Flask
from flask_restx import Api
from config import Config
from extensions import db, bcrypt, mail
from flask_cors import CORS
from sqlalchemy import text
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    # For Production later:
    # CORS(app, resources={r"/*": {"origins": "https://your-frontend-domain.com"}})

    db.init_app(app)
    bcrypt.init_app(app)
    migrate = Migrate(app, db)
    mail.init_app(app)

    # Setup Swagger / RESTX
    api = Api(
        app,
        version='1.0',
        title='Mental Health Assistant API',
        description='Documentation for PHQ-9 and GAD-7 Chatbot',
        doc='/docs'
    )

    # Register Namespaces
    from routes.auth_routes import auth_ns
    from routes.chat_routes import chat_ns
    from routes.chatbot_routes import chatbot_ns
    from routes.response_routes import response_ns

    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(chat_ns, path='/chats')
    api.add_namespace(chatbot_ns, path='/chatbot')
    api.add_namespace(response_ns, path='/responses')

    from routes.answer_routes import answer_bp
    app.register_blueprint(answer_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
            print("PostgreSQL connection established!")
        except Exception as e:
            print("Failed to connect to PostgreSQL:", e)

        db.create_all()

    print(f"📂 Using database path: {app.config['SQLALCHEMY_DATABASE_URI']}")
    app.run(debug=True)
