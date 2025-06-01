import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # SQLALCHEMY_DATABASE_URI = "sqlite:////Users/67985/Documents/mental_health_api/mental_health.db"
    # SQLALCHEMY_DATABASE_URI = "sqlite:////home/ubuntu/mental_health_api/mental_health.db"
    SQLALCHEMY_DATABASE_URI = 'postgresql://mental_health_data:capstone2025@localhost/mental_health_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
