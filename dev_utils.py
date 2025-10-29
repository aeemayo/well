"""
Development utilities and helper scripts
"""
import secrets


def generate_secret_key():
    """Generate a secure secret key for Flask"""
    return secrets.token_hex(16)


def test_api_connections():
    """Test all API connections"""
    from utils import sentiment_analyzer
    from config import Config
    
    print("🧪 Testing API Connections\n" + "="*50)
    
    # Test OpenAI Sentiment
    print("\n💭 Testing OpenAI Sentiment Analysis...")
    result = sentiment_analyzer.analyze_sentiment("I'm feeling great today!")
    if result.get('success'):
        print(f"✅ OpenAI: Sentiment={result.get('sentiment')}, Emotion={result.get('emotion')}")
        if result.get('mock'):
            print("   ⚠️ Using mock data (no API key configured)")
    else:
        print(f"❌ OpenAI error: {result.get('error')}")
    
    # Check Fitbit config
    print("\n📱 Checking Fitbit Configuration...")
    if Config.FITBIT_CLIENT_ID and Config.FITBIT_CLIENT_SECRET:
        print(f"✅ Fitbit credentials configured")
    else:
        print("⚠️ Fitbit credentials not configured (will use mock data)")
    
    # Check Spotify config
    print("\n🎵 Checking Spotify Configuration...")
    if Config.SPOTIFY_CLIENT_ID and Config.SPOTIFY_CLIENT_SECRET:
        print(f"✅ Spotify credentials configured")
    else:
        print("⚠️ Spotify credentials not configured (will use mock data)")
    
    print("\n" + "="*50)
    print("Testing complete! Check results above.")


def init_sample_data():
    """Initialize database with sample data for testing"""
    from app import app, db
    from models import User, WellnessLog
    from datetime import date, timedelta
    
    with app.app_context():
        print("🔧 Initializing sample data...")
        
        # Create sample user
        user = User.query.filter_by(username='demo').first()
        if not user:
            user = User(username='demo', email='demo@wellness.local')
            db.session.add(user)
            db.session.commit()
            print("✅ Created demo user (username: demo)")
        
        # Create sample logs
        for i in range(7):
            log_date = date.today() - timedelta(days=i)
            existing = WellnessLog.query.filter_by(user_id=user.id, date=log_date).first()
            
            if not existing:
                log = WellnessLog(
                    user_id=user.id,
                    date=log_date,
                    mood_note=f"Sample mood note for day {i+1}",
                    sentiment='positive' if i % 3 == 0 else 'neutral',
                    emotion='happy' if i % 3 == 0 else 'calm',
                    burnout_risk='low',
                    sleep_quality='good',
                    activity_level='moderate'
                )
                db.session.add(log)
        
        db.session.commit()
        print(f"✅ Created 7 days of sample wellness logs")
        print("\nYou can now login with username: demo")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python dev_utils.py [command]")
        print("\nAvailable commands:")
        print("  generate-key    - Generate a secure secret key")
        print("  test-apis       - Test all API connections")
        print("  init-sample     - Initialize sample data")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'generate-key':
        key = generate_secret_key()
        print(f"Generated secret key:\n{key}")
        print("\nAdd this to your .env file:")
        print(f"SECRET_KEY={key}")
    
    elif command == 'test-apis':
        test_api_connections()
    
    elif command == 'init-sample':
        init_sample_data()
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
