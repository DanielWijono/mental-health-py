import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # SQLALCHEMY_DATABASE_URI = "sqlite:////Users/67985/Documents/mental_health_api/mental_health.db"
    # SQLALCHEMY_DATABASE_URI = "sqlite:////home/ubuntu/mental_health_api/mental_health.db"
    SQLALCHEMY_DATABASE_URI = 'postgresql://mental_health_data:capstone2025@localhost/mental_health_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mailtrap configuration. For forgot password mechanism
    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USE_TLS = True
    MAIL_USERNAME = '1d3e6d73a21a11'
    MAIL_PASSWORD = 'c2f7d26b4d5695'
    MAIL_DEFAULT_SENDER = 'noreply@mentalhealth.com'