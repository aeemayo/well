"""
Wellness Oracle - AI-Powered Personalized Health Coach
Main Flask application with routes, database, and scheduling
"""
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from config import Config
from models import db, User, WellnessLog, DailyNudge
from agents.wellness import WellnessOrchestrator
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, date, timedelta
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Initialize wellness orchestrator with OpenRouter
orchestrator = WellnessOrchestrator(config_path='wellness_config.yaml')

# Initialize scheduler for daily nudges
scheduler = BackgroundScheduler()


# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_db():
    """Initialize database tables"""
    with app.app_context():
        db.create_all()
        logger.info("Database tables created")


# Create tables when app starts (important for production deployments)
with app.app_context():
    try:
        db.create_all()
        logger.info("Database initialized successfully")
        
        # Create upload folder if it doesn't exist
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)
            logger.info(f"Created upload folder: {Config.UPLOAD_FOLDER}")
    except Exception as e:
        logger.error(f"Error initializing application: {e}")


# ============================================================================
# MAIN ROUTES
# ============================================================================

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """User dashboard with wellness trends"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('login'))
    
    # Get recent logs (last 7 days)
    recent_logs = WellnessLog.query.filter_by(user_id=user.id)\
        .order_by(WellnessLog.date.desc())\
        .limit(7)\
        .all()
    
    return render_template('dashboard.html', user=user, logs=recent_logs)


@app.route('/log', methods=['GET', 'POST'])
def log_data():
    """Log wellness data (mood, activities, sleep)"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        # Collect form data
        mood_note = request.form.get('mood_note', '')
        manual_sleep = request.form.get('manual_sleep')
        
        # Prepare task for orchestrator
        task = {
            'user_id': user_id,
            'date': date.today(),
            'mood_note': mood_note,
            'manual_sleep': {
                'minutes_asleep': float(manual_sleep) * 60 if manual_sleep else None,
                'date': 'today'
            } if manual_sleep else None,
            'fitbit_tokens': {
                'access': user.fitbit_access_token,
                'refresh': user.fitbit_refresh_token
            } if user.fitbit_access_token else None,
            'spotify_enabled': bool(user.spotify_access_token),
            'user_preferences': user.get_preferences(),
            'user_history': _get_user_history(user_id)
        }
        
        try:
            # Run wellness workflow through orchestrator
            logger.info(f"Running orchestrator for user {user_id}")
            insights = orchestrator.solve(task)
            logger.info(f"Orchestrator returned: sentiment={insights.get('sentiment')}, emotion={insights.get('emotion')}")
            
            # Check if orchestrator returned valid data
            if not insights or not insights.get('sentiment'):
                logger.error(f"Orchestrator returned invalid data: {insights}")
                flash('Error: Unable to process wellness data. Please try again.', 'error')
                return redirect(url_for('log_data'))
            
            # Save log to database
            log = WellnessLog(
                user_id=user_id,
                date=date.today(),
                mood_note=mood_note,
                manual_sleep_hours=float(manual_sleep) if manual_sleep else None,
                sentiment=insights.get('sentiment'),
                emotion=insights.get('emotion'),
                burnout_risk=insights.get('burnout_risk'),
                sleep_quality=insights.get('sleep_quality'),
                activity_level=insights.get('activity_level')
            )
            
            logger.info(f"Created log with sentiment={log.sentiment}, emotion={log.emotion}")
            
            # Store JSON data
            if insights.get('data_summary'):
                log.set_sleep_data({'hours': insights['data_summary'].get('sleep_hours')})
                log.set_activity_data({
                    'steps': insights['data_summary'].get('steps'),
                    'active_minutes': insights['data_summary'].get('active_minutes')
                })
            
            log.set_recommendations({
                'micro_habits': insights.get('micro_habits', []),
                'interventions': insights.get('interventions', []),
                'playlist': insights.get('playlist')
            })
            
            db.session.add(log)
            db.session.commit()
            logger.info(f"Successfully committed log to database")
            
            flash('Wellness data logged successfully!', 'success')
            return render_template('insights.html', insights=insights, log=log)
            
        except Exception as e:
            logger.error(f"Error processing wellness data: {str(e)}", exc_info=True)
            db.session.rollback()
            flash(f'Error processing data: {str(e)}', 'error')
            return redirect(url_for('log_data'))
    
    return render_template('log.html')


@app.route('/oracle', methods=['GET', 'POST'])
def oracle():
    """Chat-like oracle interface for asking wellness questions"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        query = request.form.get('query', '')
        
        # Simple query handling (can be enhanced with LLM)
        response = _handle_oracle_query(query, session['user_id'])
        
        return jsonify(response)
    
    return render_template('oracle.html')


@app.route('/history')
def history():
    """View historical wellness data"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    # Get all logs for the user
    logs = WellnessLog.query.filter_by(user_id=user_id)\
        .order_by(WellnessLog.date.desc())\
        .all()
    
    return render_template('history.html', logs=logs)


# ============================================================================
# AUTHENTICATION ROUTES (Simple Session-based)
# ============================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Simple login (username only for MVP)"""
    if request.method == 'POST':
        username = request.form.get('username')
        
        if not username:
            flash('Username required', 'error')
            return redirect(url_for('login'))
        
        # Find or create user
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
            flash(f'Welcome, {username}! Account created.', 'success')
        else:
            flash(f'Welcome back, {username}!', 'success')
        
        session['user_id'] = user.id
        session['username'] = user.username
        
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('index'))


# ============================================================================
# OAUTH CALLBACK ROUTES
# ============================================================================

@app.route('/fitbit/auth')
def fitbit_auth():
    """Redirect to Fitbit OAuth"""
    from utils import FitbitClient
    
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        auth_url = FitbitClient.get_auth_url()
        return redirect(auth_url)
    except Exception as e:
        flash(f'Fitbit authentication error: {str(e)}', 'error')
        return redirect(url_for('dashboard'))


@app.route('/fitbit/callback')
def fitbit_callback():
    """Handle Fitbit OAuth callback"""
    from utils import FitbitClient
    
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    code = request.args.get('code')
    if not code:
        flash('Fitbit authorization failed', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        # Exchange code for tokens
        tokens = FitbitClient.exchange_code_for_token(code)
        
        # Store tokens in database
        user = User.query.get(session['user_id'])
        user.fitbit_access_token = tokens['access_token']
        user.fitbit_refresh_token = tokens['refresh_token']
        db.session.commit()
        
        flash('Fitbit connected successfully!', 'success')
    except Exception as e:
        flash(f'Error connecting Fitbit: {str(e)}', 'error')
    
    return redirect(url_for('dashboard'))


@app.route('/spotify/auth')
def spotify_auth():
    """Redirect to Spotify OAuth"""
    from utils import SpotifyClient
    
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        auth_manager = SpotifyClient.get_auth_manager()
        auth_url = auth_manager.get_authorize_url()
        return redirect(auth_url)
    except Exception as e:
        flash(f'Spotify authentication error: {str(e)}', 'error')
        return redirect(url_for('dashboard'))


@app.route('/spotify/callback')
def spotify_callback():
    """Handle Spotify OAuth callback"""
    from utils import SpotifyClient
    
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    code = request.args.get('code')
    if not code:
        flash('Spotify authorization failed', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        # Exchange code for tokens
        auth_manager = SpotifyClient.get_auth_manager()
        tokens = auth_manager.get_access_token(code)
        
        # Store tokens
        user = User.query.get(session['user_id'])
        user.spotify_access_token = tokens['access_token']
        user.spotify_refresh_token = tokens['refresh_token']
        db.session.commit()
        
        flash('Spotify connected successfully!', 'success')
    except Exception as e:
        flash(f'Error connecting Spotify: {str(e)}', 'error')
    
    return redirect(url_for('dashboard'))


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _get_user_history(user_id: int, days: int = 7) -> list:
    """Get user's wellness history for adaptation"""
    cutoff_date = date.today() - timedelta(days=days)
    
    logs = WellnessLog.query.filter(
        WellnessLog.user_id == user_id,
        WellnessLog.date >= cutoff_date
    ).order_by(WellnessLog.date.asc()).all()
    
    history = []
    for log in logs:
        sleep_data = log.get_sleep_data()
        history.append({
            'date': log.date.isoformat(),
            'sentiment': log.sentiment,
            'sleep_minutes': sleep_data.get('hours', 0) * 60 if sleep_data.get('hours') else 0,
            'burnout_risk': log.burnout_risk
        })
    
    return history


def _handle_oracle_query(query: str, user_id: int) -> dict:
    """Handle oracle chat queries (simplified for MVP)"""
    query_lower = query.lower()
    
    # Simple keyword matching (can be replaced with LLM)
    if 'sleep' in query_lower:
        recent_log = WellnessLog.query.filter_by(user_id=user_id)\
            .order_by(WellnessLog.date.desc()).first()
        
        if recent_log:
            sleep_data = recent_log.get_sleep_data()
            return {
                'response': f"Your recent sleep quality is {recent_log.sleep_quality}. "
                           f"You slept about {sleep_data.get('hours', 'unknown')} hours.",
                'type': 'sleep_info'
            }
    
    elif 'burnout' in query_lower or 'stress' in query_lower:
        recent_log = WellnessLog.query.filter_by(user_id=user_id)\
            .order_by(WellnessLog.date.desc()).first()
        
        if recent_log:
            recs = recent_log.get_recommendations()
            return {
                'response': f"Your burnout risk is {recent_log.burnout_risk}. "
                           f"Here are some interventions: {', '.join(recs.get('interventions', []))}",
                'type': 'burnout_info'
            }
    
    return {
        'response': "I'm here to help with your wellness! Try asking about sleep, stress, or mood.",
        'type': 'general'
    }


# ============================================================================
# SCHEDULED TASKS
# ============================================================================

def send_daily_nudges():
    """Send daily wellness nudges to users"""
    logger.info("Running daily nudge job...")
    
    # Get all users who haven't logged today
    today = date.today()
    users = User.query.all()
    
    for user in users:
        # Check if user logged today
        log_today = WellnessLog.query.filter_by(
            user_id=user.id,
            date=today
        ).first()
        
        if not log_today:
            # Send nudge (in production: email or push notification)
            logger.info(f"Nudge sent to user {user.username}: Don't forget your wellness check-in!")
            
            # Record nudge
            nudge = DailyNudge(
                user_id=user.id,
                message="Time for your daily wellness check-in!",
                sent_at=datetime.now()
            )
            db.session.add(nudge)
    
    db.session.commit()
    logger.info("Daily nudge job completed")


# ============================================================================
# APPLICATION INITIALIZATION
# ============================================================================

def init_app():
    """Initialize application (for local development)"""
    with app.app_context():
        # Create upload folder if it doesn't exist
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)
        
        # Start scheduler
        if not scheduler.running:
            scheduler.add_job(
                func=send_daily_nudges,
                trigger='cron',
                hour=8,
                minute=0,
                id='daily_nudges'
            )
            scheduler.start()
            logger.info("Scheduler started")


if __name__ == '__main__':
    init_app()
    
    try:
        app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Application shutdown")
