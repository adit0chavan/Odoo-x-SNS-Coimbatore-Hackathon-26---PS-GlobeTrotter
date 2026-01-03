import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///globetrotter.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TAVILY_API_KEY = 'YOUR_API_KEY' # Tavily API Key
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'app/static/uploads'
