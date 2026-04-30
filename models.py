"""
Firestore database models for Wellness Oracle
Replaces SQLAlchemy with Firebase Cloud Firestore
"""
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import FieldFilter
from datetime import datetime, date, time
import json
import os
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# FIRESTORE INITIALIZATION
# ============================================================================

_firestore_client = None


def get_db():
    """Get Firestore client (lazy initialization)"""
    global _firestore_client
    if _firestore_client is None:
        _firestore_client = _init_firestore()
    return _firestore_client


def _init_firestore():
    """Initialize Firebase Admin SDK and return Firestore client"""
    try:
        if not firebase_admin._apps:
            cred_json_str = os.getenv('FIREBASE_CREDENTIALS_JSON')
            cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH')
            
            if cred_json_str:
                # Load credentials directly from a JSON string (great for Render env vars)
                import json
                cred_dict = json.loads(cred_json_str)
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
                logger.info("Firebase initialized using FIREBASE_CREDENTIALS_JSON env var")
            elif cred_path and os.path.exists(cred_path):
                # Load credentials from file
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                logger.info(f"Firebase initialized with service account: {cred_path}")
            else:
                # Fallback to default
                firebase_admin.initialize_app()
                logger.info("Firebase initialized with default credentials")
        return firestore.client()
    except Exception as e:
        logger.error(f"Failed to initialize Firestore: {e}")
        raise


# ============================================================================
# SERIALIZATION HELPERS
# ============================================================================

def _serialize_date(d):
    """Convert date/datetime to ISO string for Firestore storage"""
    if isinstance(d, datetime):
        return d.isoformat()
    elif isinstance(d, date):
        return d.isoformat()
    return str(d) if d else None


def _deserialize_date(s):
    """Convert ISO string back to date object"""
    if isinstance(s, date) and not isinstance(s, datetime):
        return s
    if isinstance(s, datetime):
        return s.date()
    if s:
        try:
            return date.fromisoformat(str(s))
        except (ValueError, TypeError):
            return None
    return None


def _deserialize_datetime(s):
    """Convert ISO string back to datetime object"""
    if isinstance(s, datetime):
        return s
    if s:
        try:
            return datetime.fromisoformat(str(s))
        except (ValueError, TypeError):
            return None
    return None


# ============================================================================
# USER MODEL
# ============================================================================

class User:
    """User document model — Firestore collection: 'users'"""
    COLLECTION = 'users'

    def __init__(self, id=None, username=None, email=None, created_at=None,
                 fitbit_access_token=None, fitbit_refresh_token=None,
                 spotify_access_token=None, spotify_refresh_token=None,
                 preferences=None):
        self.id = id
        self.username = username
        self.email = email
        self.created_at = created_at or datetime.utcnow()
        self.fitbit_access_token = fitbit_access_token
        self.fitbit_refresh_token = fitbit_refresh_token
        self.spotify_access_token = spotify_access_token
        self.spotify_refresh_token = spotify_refresh_token
        self.preferences = preferences or '{}'

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'created_at': _serialize_date(self.created_at),
            'fitbit_access_token': self.fitbit_access_token,
            'fitbit_refresh_token': self.fitbit_refresh_token,
            'spotify_access_token': self.spotify_access_token,
            'spotify_refresh_token': self.spotify_refresh_token,
            'preferences': self.preferences,
        }

    @classmethod
    def from_doc(cls, doc):
        """Create User from Firestore DocumentSnapshot"""
        if not doc.exists:
            return None
        data = doc.to_dict()
        return cls(
            id=doc.id,
            username=data.get('username'),
            email=data.get('email'),
            created_at=_deserialize_datetime(data.get('created_at')),
            fitbit_access_token=data.get('fitbit_access_token'),
            fitbit_refresh_token=data.get('fitbit_refresh_token'),
            spotify_access_token=data.get('spotify_access_token'),
            spotify_refresh_token=data.get('spotify_refresh_token'),
            preferences=data.get('preferences', '{}'),
        )

    # ---- CRUD ----

    def save(self):
        """Create or update this user document"""
        db = get_db()
        if self.id:
            db.collection(self.COLLECTION).document(self.id).set(self.to_dict())
        else:
            _, doc_ref = db.collection(self.COLLECTION).add(self.to_dict())
            self.id = doc_ref.id
        return self

    def delete(self):
        if self.id:
            get_db().collection(self.COLLECTION).document(self.id).delete()

    # ---- Queries ----

    @classmethod
    def get_by_id(cls, user_id):
        if not user_id:
            return None
        doc = get_db().collection(cls.COLLECTION).document(str(user_id)).get()
        return cls.from_doc(doc)

    @classmethod
    def get_by_username(cls, username):
        docs = get_db().collection(cls.COLLECTION)\
            .where(filter=FieldFilter('username', '==', username))\
            .limit(1).stream()
        for doc in docs:
            return cls.from_doc(doc)
        return None

    @classmethod
    def get_all(cls):
        return [cls.from_doc(d) for d in get_db().collection(cls.COLLECTION).stream()]

    # ---- Helpers ----

    def get_preferences(self):
        try:
            return json.loads(self.preferences) if self.preferences else {}
        except Exception:
            return {}

    def set_preferences(self, prefs_dict):
        self.preferences = json.dumps(prefs_dict)

    def __repr__(self):
        return f'<User {self.username}>'


# ============================================================================
# WELLNESS LOG MODEL
# ============================================================================

class WellnessLog:
    """Daily wellness log — Firestore collection: 'wellness_logs'"""
    COLLECTION = 'wellness_logs'

    def __init__(self, id=None, user_id=None, date=None, created_at=None,
                 mood_note=None, meal_description=None, manual_sleep_hours=None,
                 sentiment=None, emotion=None, burnout_risk=None,
                 sleep_quality=None, activity_level=None,
                 sleep_data=None, activity_data=None, nutrition_data=None,
                 recommendations=None):
        self.id = id
        self.user_id = user_id
        self.date = date
        self.created_at = created_at or datetime.utcnow()
        self.mood_note = mood_note
        self.meal_description = meal_description
        self.manual_sleep_hours = manual_sleep_hours
        self.sentiment = sentiment
        self.emotion = emotion
        self.burnout_risk = burnout_risk
        self.sleep_quality = sleep_quality
        self.activity_level = activity_level
        self.sleep_data = sleep_data
        self.activity_data = activity_data
        self.nutrition_data = nutrition_data
        self.recommendations = recommendations

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'date': _serialize_date(self.date),
            'created_at': _serialize_date(self.created_at),
            'mood_note': self.mood_note,
            'meal_description': self.meal_description,
            'manual_sleep_hours': self.manual_sleep_hours,
            'sentiment': self.sentiment,
            'emotion': self.emotion,
            'burnout_risk': self.burnout_risk,
            'sleep_quality': self.sleep_quality,
            'activity_level': self.activity_level,
            'sleep_data': self.sleep_data,
            'activity_data': self.activity_data,
            'nutrition_data': self.nutrition_data,
            'recommendations': self.recommendations,
        }

    @classmethod
    def from_doc(cls, doc):
        if not doc.exists:
            return None
        data = doc.to_dict()
        return cls(
            id=doc.id,
            user_id=data.get('user_id'),
            date=_deserialize_date(data.get('date')),
            created_at=_deserialize_datetime(data.get('created_at')),
            mood_note=data.get('mood_note'),
            meal_description=data.get('meal_description'),
            manual_sleep_hours=data.get('manual_sleep_hours'),
            sentiment=data.get('sentiment'),
            emotion=data.get('emotion'),
            burnout_risk=data.get('burnout_risk'),
            sleep_quality=data.get('sleep_quality'),
            activity_level=data.get('activity_level'),
            sleep_data=data.get('sleep_data'),
            activity_data=data.get('activity_data'),
            nutrition_data=data.get('nutrition_data'),
            recommendations=data.get('recommendations'),
        )

    # ---- CRUD ----

    def save(self):
        db = get_db()
        if self.id:
            db.collection(self.COLLECTION).document(self.id).set(self.to_dict())
        else:
            _, doc_ref = db.collection(self.COLLECTION).add(self.to_dict())
            self.id = doc_ref.id
        return self

    def delete(self):
        if self.id:
            get_db().collection(self.COLLECTION).document(self.id).delete()

    # ---- Queries ----

    @classmethod
    def get_by_user(cls, user_id, order_desc=True, limit=None):
        """Fetch logs for a user, ordered by date."""
        direction = firestore.Query.DESCENDING if order_desc else firestore.Query.ASCENDING
        query = get_db().collection(cls.COLLECTION)\
            .where(filter=FieldFilter('user_id', '==', user_id))\
            .order_by('date', direction=direction)
        if limit:
            query = query.limit(limit)
        return [cls.from_doc(d) for d in query.stream()]

    @classmethod
    def get_by_user_and_date(cls, user_id, target_date):
        """Fetch a single log for a user on a specific date."""
        date_str = _serialize_date(target_date)
        docs = get_db().collection(cls.COLLECTION)\
            .where(filter=FieldFilter('user_id', '==', user_id))\
            .where(filter=FieldFilter('date', '==', date_str))\
            .limit(1).stream()
        for doc in docs:
            return cls.from_doc(doc)
        return None

    @classmethod
    def get_by_user_since(cls, user_id, cutoff_date, order_asc=True):
        """Fetch logs for a user since a cutoff date."""
        date_str = _serialize_date(cutoff_date)
        direction = firestore.Query.ASCENDING if order_asc else firestore.Query.DESCENDING
        query = get_db().collection(cls.COLLECTION)\
            .where(filter=FieldFilter('user_id', '==', user_id))\
            .where(filter=FieldFilter('date', '>=', date_str))\
            .order_by('date', direction=direction)
        return [cls.from_doc(d) for d in query.stream()]

    @classmethod
    def get_latest_by_user(cls, user_id):
        """Fetch the most recent log for a user."""
        docs = get_db().collection(cls.COLLECTION)\
            .where(filter=FieldFilter('user_id', '==', user_id))\
            .order_by('date', direction=firestore.Query.DESCENDING)\
            .limit(1).stream()
        for doc in docs:
            return cls.from_doc(doc)
        return None

    # ---- JSON field helpers ----

    def get_sleep_data(self):
        try:
            return json.loads(self.sleep_data) if self.sleep_data else {}
        except Exception:
            return {}

    def set_sleep_data(self, data_dict):
        self.sleep_data = json.dumps(data_dict)

    def get_activity_data(self):
        try:
            return json.loads(self.activity_data) if self.activity_data else {}
        except Exception:
            return {}

    def set_activity_data(self, data_dict):
        self.activity_data = json.dumps(data_dict)

    def get_nutrition_data(self):
        try:
            return json.loads(self.nutrition_data) if self.nutrition_data else {}
        except Exception:
            return {}

    def set_nutrition_data(self, data_dict):
        self.nutrition_data = json.dumps(data_dict)

    def get_recommendations(self):
        try:
            return json.loads(self.recommendations) if self.recommendations else {}
        except Exception:
            return {}

    def set_recommendations(self, rec_dict):
        self.recommendations = json.dumps(rec_dict)

    def __repr__(self):
        return f'<WellnessLog user_id={self.user_id} date={self.date}>'


# ============================================================================
# DAILY NUDGE MODEL
# ============================================================================

class DailyNudge:
    """Scheduled daily nudges — Firestore collection: 'daily_nudges'"""
    COLLECTION = 'daily_nudges'

    def __init__(self, id=None, user_id=None, scheduled_time=None,
                 message=None, sent_at=None):
        self.id = id
        self.user_id = user_id
        self.scheduled_time = scheduled_time or datetime.strptime('08:00', '%H:%M').time()
        self.message = message
        self.sent_at = sent_at

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else '08:00:00',
            'message': self.message,
            'sent_at': _serialize_date(self.sent_at),
        }

    @classmethod
    def from_doc(cls, doc):
        if not doc.exists:
            return None
        data = doc.to_dict()
        sched = data.get('scheduled_time')
        if isinstance(sched, str):
            try:
                sched = time.fromisoformat(sched)
            except (ValueError, TypeError):
                sched = time(8, 0)
        return cls(
            id=doc.id,
            user_id=data.get('user_id'),
            scheduled_time=sched,
            message=data.get('message'),
            sent_at=_deserialize_datetime(data.get('sent_at')),
        )

    def save(self):
        db = get_db()
        if self.id:
            db.collection(self.COLLECTION).document(self.id).set(self.to_dict())
        else:
            _, doc_ref = db.collection(self.COLLECTION).add(self.to_dict())
            self.id = doc_ref.id
        return self

    def __repr__(self):
        return f'<DailyNudge user_id={self.user_id} time={self.scheduled_time}>'
