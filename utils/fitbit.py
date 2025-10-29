"""
Fitbit API integration for wearable data (sleep, activity, heart rate)
"""
from fitbit import Fitbit
from fitbit.api import FitbitOauth2Client
from flask import session
from config import Config
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class FitbitClient:
    """Wrapper for Fitbit API with OAuth2 support"""
    
    @staticmethod
    def get_auth_url():
        """Get the OAuth2 authorization URL"""
        oauth = FitbitOauth2Client(
            Config.FITBIT_CLIENT_ID,
            Config.FITBIT_CLIENT_SECRET,
            redirect_uri=Config.FITBIT_REDIRECT_URI
        )
        url, _ = oauth.authorize_token_url(
            scope=['activity', 'heartrate', 'sleep', 'profile']
        )
        return url
    
    @staticmethod
    def exchange_code_for_token(code: str):
        """Exchange authorization code for access token"""
        oauth = FitbitOauth2Client(
            Config.FITBIT_CLIENT_ID,
            Config.FITBIT_CLIENT_SECRET,
            redirect_uri=Config.FITBIT_REDIRECT_URI
        )
        return oauth.fetch_access_token(code)
    
    @staticmethod
    def get_client(access_token: str = None, refresh_token: str = None):
        """
        Get an authenticated Fitbit client
        
        Args:
            access_token: OAuth2 access token (from session if not provided)
            refresh_token: OAuth2 refresh token (from session if not provided)
            
        Returns:
            Fitbit: Authenticated Fitbit client instance
        """
        if not access_token:
            access_token = session.get('fitbit_access_token')
        if not refresh_token:
            refresh_token = session.get('fitbit_refresh_token')
        
        if not access_token or not refresh_token:
            raise ValueError("Fitbit tokens not found in session")
        
        return Fitbit(
            Config.FITBIT_CLIENT_ID,
            Config.FITBIT_CLIENT_SECRET,
            oauth2=True,
            access_token=access_token,
            refresh_token=refresh_token
        )
    
    @staticmethod
    def fetch_sleep(date='today', access_token=None, refresh_token=None) -> dict:
        """
        Fetch sleep data for a specific date
        
        Args:
            date: Date string (YYYY-MM-DD) or 'today'
            
        Returns:
            dict: Sleep data including duration, stages, efficiency
        """
        try:
            client = FitbitClient.get_client(access_token, refresh_token)
            sleep_data = client.sleep(date=date)
            
            if sleep_data.get('sleep') and len(sleep_data['sleep']) > 0:
                main_sleep = sleep_data['sleep'][0]
                return {
                    'date': date,
                    'duration_minutes': main_sleep.get('duration', 0) // 60000,  # Convert ms to minutes
                    'efficiency': main_sleep.get('efficiency', 0),
                    'start_time': main_sleep.get('startTime'),
                    'end_time': main_sleep.get('endTime'),
                    'minutes_asleep': main_sleep.get('minutesAsleep', 0),
                    'minutes_awake': main_sleep.get('minutesAwake', 0),
                    'success': True
                }
            else:
                return {'success': False, 'error': 'No sleep data found'}
                
        except Exception as e:
            logger.error(f"Error fetching sleep data: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def fetch_activity(date='today', access_token=None, refresh_token=None) -> dict:
        """
        Fetch activity data for a specific date
        
        Args:
            date: Date string (YYYY-MM-DD) or 'today'
            
        Returns:
            dict: Activity data including steps, calories, distance
        """
        try:
            client = FitbitClient.get_client(access_token, refresh_token)
            activity_data = client.activities(date=date)
            
            summary = activity_data.get('summary', {})
            return {
                'date': date,
                'steps': summary.get('steps', 0),
                'calories': summary.get('caloriesOut', 0),
                'distance': summary.get('distances', [{}])[0].get('distance', 0),
                'active_minutes': summary.get('fairlyActiveMinutes', 0) + summary.get('veryActiveMinutes', 0),
                'sedentary_minutes': summary.get('sedentaryMinutes', 0),
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error fetching activity data: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def fetch_heart_rate(date='today', access_token=None, refresh_token=None) -> dict:
        """
        Fetch heart rate data for a specific date
        
        Args:
            date: Date string (YYYY-MM-DD) or 'today'
            
        Returns:
            dict: Heart rate data including resting HR and zones
        """
        try:
            client = FitbitClient.get_client(access_token, refresh_token)
            hr_data = client.intraday_time_series('activities/heart', base_date=date, detail_level='1min')
            
            activities = hr_data.get('activities-heart', [{}])[0]
            value = activities.get('value', {})
            
            return {
                'date': date,
                'resting_heart_rate': value.get('restingHeartRate', 0),
                'heart_rate_zones': value.get('heartRateZones', []),
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error fetching heart rate data: {str(e)}")
            return {'success': False, 'error': str(e)}


# Mock data generator for testing without Fitbit connection
def mock_fitbit_data(date='today'):
    """Generate mock Fitbit data for testing"""
    return {
        'sleep': {
            'date': date,
            'duration_minutes': 420,  # 7 hours
            'efficiency': 85,
            'start_time': '23:00:00',
            'end_time': '06:00:00',
            'minutes_asleep': 400,
            'minutes_awake': 20,
            'success': True,
            'mock': True
        },
        'activity': {
            'date': date,
            'steps': 8500,
            'calories': 2200,
            'distance': 6.5,
            'active_minutes': 45,
            'sedentary_minutes': 480,
            'success': True,
            'mock': True
        }
    }
