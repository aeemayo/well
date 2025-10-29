import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///users.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # API Keys
    FITBIT_CLIENT_ID = os.getenv('FITBIT_CLIENT_ID')
    FITBIT_CLIENT_SECRET = os.getenv('FITBIT_CLIENT_SECRET')
    FITBIT_REDIRECT_URI = os.getenv('FITBIT_REDIRECT_URI', 'http://localhost:5000/fitbit/callback')
    
    SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:5000/spotify/callback')
    
    # OpenRouter API (using OpenAI-compatible interface)
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL', 'deepseek/deepseek-chat')
    
    # For OpenAI SDK compatibility
    OPENAI_API_KEY = os.getenv('OPENROUTER_API_KEY')
    
    # Upload settings
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
