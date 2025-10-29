"""
Database models for Wellness Oracle
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()


class User(db.Model):
    """User model for storing user profiles and preferences"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # OAuth tokens (encrypted in production!)
    fitbit_access_token = db.Column(db.Text, nullable=True)
    fitbit_refresh_token = db.Column(db.Text, nullable=True)
    spotify_access_token = db.Column(db.Text, nullable=True)
    spotify_refresh_token = db.Column(db.Text, nullable=True)
    
    # User preferences (stored as JSON)
    preferences = db.Column(db.Text, default='{}')
    
    # Relationships
    logs = db.relationship('WellnessLog', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def get_preferences(self):
        """Parse preferences JSON"""
        try:
            return json.loads(self.preferences) if self.preferences else {}
        except:
            return {}
    
    def set_preferences(self, prefs_dict):
        """Store preferences as JSON"""
        self.preferences = json.dumps(prefs_dict)
    
    def __repr__(self):
        return f'<User {self.username}>'


class WellnessLog(db.Model):
    """Daily wellness log entries"""
    __tablename__ = 'wellness_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # User inputs
    mood_note = db.Column(db.Text, nullable=True)
    meal_description = db.Column(db.Text, nullable=True)
    manual_sleep_hours = db.Column(db.Float, nullable=True)
    
    # Analysis results (stored as JSON)
    sentiment = db.Column(db.String(20), nullable=True)
    emotion = db.Column(db.String(50), nullable=True)
    burnout_risk = db.Column(db.String(20), nullable=True)
    sleep_quality = db.Column(db.String(20), nullable=True)
    activity_level = db.Column(db.String(20), nullable=True)
    
    # Data summary (JSON)
    sleep_data = db.Column(db.Text, nullable=True)  # JSON: Fitbit or manual
    activity_data = db.Column(db.Text, nullable=True)  # JSON: Fitbit
    nutrition_data = db.Column(db.Text, nullable=True)  # JSON: Nutritionix
    
    # Recommendations (JSON)
    recommendations = db.Column(db.Text, nullable=True)
    
    def get_sleep_data(self):
        try:
            return json.loads(self.sleep_data) if self.sleep_data else {}
        except:
            return {}
    
    def set_sleep_data(self, data_dict):
        self.sleep_data = json.dumps(data_dict)
    
    def get_activity_data(self):
        try:
            return json.loads(self.activity_data) if self.activity_data else {}
        except:
            return {}
    
    def set_activity_data(self, data_dict):
        self.activity_data = json.dumps(data_dict)
    
    def get_nutrition_data(self):
        try:
            return json.loads(self.nutrition_data) if self.nutrition_data else {}
        except:
            return {}
    
    def set_nutrition_data(self, data_dict):
        self.nutrition_data = json.dumps(data_dict)
    
    def get_recommendations(self):
        try:
            return json.loads(self.recommendations) if self.recommendations else {}
        except:
            return {}
    
    def set_recommendations(self, rec_dict):
        self.recommendations = json.dumps(rec_dict)
    
    def __repr__(self):
        return f'<WellnessLog user_id={self.user_id} date={self.date}>'


class DailyNudge(db.Model):
    """Scheduled daily nudges/reminders"""
    __tablename__ = 'daily_nudges'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    scheduled_time = db.Column(db.Time, default=datetime.strptime('08:00', '%H:%M').time())
    message = db.Column(db.Text, nullable=True)
    sent_at = db.Column(db.DateTime, nullable=True)
    
    user = db.relationship('User', backref='nudges')
    
    def __repr__(self):
        return f'<DailyNudge user_id={self.user_id} time={self.scheduled_time}>'
