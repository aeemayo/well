"""
Wellness workflow orchestrator for wellness data processing
Implements hierarchical task decomposition and agent execution
"""
import yaml
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
from utils import (
    sentiment_analyzer, 
    FitbitClient, 
    mock_fitbit_data,
    SpotifyClient,
    mock_mood_playlist
)

logger = logging.getLogger(__name__)


class WellnessOrchestrator:
    """
    Root orchestrator for wellness data analysis and recommendation generation
    """
    
    def __init__(self, config_path: str = 'wellness_config.yaml'):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.agents = {
            'ingestion': IngestionAgent(self.config),
            'analysis': AnalysisAgent(self.config),
            'recommendation': RecommendationAgent(self.config),
            'synthesis': SynthesisAgent(self.config)
        }
    
    def solve(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point: recursively decompose and execute wellness workflow
        
        Args:
            task: User task containing:
                - user_id: User identifier
                - date: Target date for analysis
                - mood_note: User's mood/journal entry
                - meal: Meal description (optional)
                - manual_sleep: Manual sleep entry (optional)
                
        Returns:
            dict: Synthesized wellness insights and recommendations
        """
        logger.info(f"Starting wellness workflow for user {task.get('user_id')}")
        
        try:
            # Phase 1: Data Ingestion
            ingestion_result = self.agents['ingestion'].execute(task)
            
            # Phase 2: Analysis
            analysis_task = {**task, 'ingestion_data': ingestion_result}
            analysis_result = self.agents['analysis'].execute(analysis_task)
            
            # Phase 3: Recommendation Generation
            rec_task = {**task, 'analysis_data': analysis_result}
            recommendation_result = self.agents['recommendation'].execute(rec_task)
            
            # Phase 4: Synthesis & Personalization
            synthesis_task = {
                **task,
                'ingestion_data': ingestion_result,
                'analysis_data': analysis_result,
                'recommendations': recommendation_result
            }
            final_result = self.agents['synthesis'].execute(synthesis_task)
            
            logger.info("Wellness workflow completed successfully")
            return final_result
            
        except Exception as e:
            logger.error(f"Workflow error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'fallback_recommendations': self._generate_fallback()
            }
    
    def _generate_fallback(self) -> Dict[str, Any]:
        """Generate basic recommendations when workflow fails"""
        return {
            'success': False,
            'habits': [
                "Take a 10-minute walk outside",
                "Practice 5 minutes of deep breathing",
                "Drink a glass of water"
            ],
            'message': "Basic wellness recommendations (limited data available)",
            'sentiment': 'neutral',
            'emotion': 'calm',
            'burnout_risk': 'unknown',
            'sleep_quality': 'unknown',
            'activity_level': 'unknown',
            'micro_habits': [
                "Take a 10-minute walk outside",
                "Practice 5 minutes of deep breathing",
                "Drink a glass of water"
            ],
            'data_summary': {
                'sleep_hours': 0,
                'steps': 0,
                'active_minutes': 0,
                'calories': 'N/A'
            }
        }


class IngestionAgent:
    """Agent responsible for fetching and preprocessing data from all sources"""
    
    def __init__(self, config: Dict):
        self.config = config
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch data from Fitbit, nutrition APIs, and user inputs
        
        Returns:
            dict: Aggregated data from all sources
        """
        logger.info("Ingestion Agent: Fetching data...")
        
        result = {
            'sleep': None,
            'activity': None,
            'nutrition': None,
            'mood_text': task.get('mood_note', ''),
            'timestamp': datetime.now().isoformat()
        }
        
        # Fetch Fitbit sleep data (or use manual entry)
        if task.get('manual_sleep'):
            result['sleep'] = task['manual_sleep']
        elif task.get('fitbit_tokens'):
            try:
                result['sleep'] = FitbitClient.fetch_sleep(
                    date=task.get('date', 'today'),
                    access_token=task['fitbit_tokens'].get('access'),
                    refresh_token=task['fitbit_tokens'].get('refresh')
                )
            except Exception as e:
                logger.warning(f"Fitbit sleep fetch failed: {e}, using mock data")
                result['sleep'] = mock_fitbit_data()['sleep']
        else:
            result['sleep'] = mock_fitbit_data()['sleep']
        
        # Fetch Fitbit activity data
        if task.get('fitbit_tokens'):
            try:
                result['activity'] = FitbitClient.fetch_activity(
                    date=task.get('date', 'today'),
                    access_token=task['fitbit_tokens'].get('access'),
                    refresh_token=task['fitbit_tokens'].get('refresh')
                )
            except Exception as e:
                logger.warning(f"Fitbit activity fetch failed: {e}, using mock data")
                result['activity'] = mock_fitbit_data()['activity']
        else:
            result['activity'] = mock_fitbit_data()['activity']
        
        # Analyze meal if provided
        if task.get('meal'):
            result['nutrition'] = nutrition_analyzer.analyze_meal(task['meal'])
        
        logger.info("Ingestion Agent: Data collection complete")
        return result


class AnalysisAgent:
    """Agent for sentiment analysis and burnout risk prediction"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.burnout_thresholds = config['tools']['burnout_predictor']['thresholds']
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze sentiment and predict burnout risk
        
        Returns:
            dict: Sentiment, emotion, and risk assessments
        """
        logger.info("Analysis Agent: Starting analysis...")
        
        ingestion_data = task.get('ingestion_data', {})
        
        # Sentiment analysis on mood note
        sentiment_result = sentiment_analyzer.analyze_sentiment(
            ingestion_data.get('mood_text', 'neutral day')
        )
        
        # Burnout risk prediction
        burnout_risk = self._predict_burnout(
            sleep_data=ingestion_data.get('sleep', {}),
            activity_data=ingestion_data.get('activity', {}),
            sentiment=sentiment_result.get('sentiment'),
            user_history=task.get('user_history', [])
        )
        
        # Sleep quality assessment
        sleep_quality = self._assess_sleep_quality(ingestion_data.get('sleep', {}))
        
        # Activity level assessment
        activity_level = self._assess_activity(ingestion_data.get('activity', {}))
        
        result = {
            'sentiment': sentiment_result.get('sentiment'),
            'emotion': sentiment_result.get('emotion'),
            'burnout_risk': burnout_risk,
            'sleep_quality': sleep_quality,
            'activity_level': activity_level,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Analysis Agent: Complete - Risk: {burnout_risk}, Sentiment: {sentiment_result.get('sentiment')}")
        return result
    
    def _predict_burnout(self, sleep_data: Dict, activity_data: Dict, sentiment: str, user_history: List) -> str:
        """
        Predict burnout risk based on multiple factors
        
        Returns:
            str: 'low', 'medium', or 'high'
        """
        risk_score = 0
        
        # Factor 1: Sleep duration
        sleep_minutes = sleep_data.get('minutes_asleep', 420)
        sleep_minimum = self.burnout_thresholds.get('sleep_minimum', self.burnout_thresholds.get('sleep_hours_min', 6.0) * 60)
        if sleep_minutes < sleep_minimum:
            risk_score += 2
        elif sleep_minutes < 420:  # Less than 7 hours
            risk_score += 1
        
        # Factor 2: Activity level
        active_minutes = activity_data.get('active_minutes', 30)
        activity_minimum = self.burnout_thresholds.get('activity_minimum', 30)
        if active_minutes < activity_minimum:
            risk_score += 1
        
        # Factor 3: Sentiment
        if sentiment == 'negative':
            risk_score += 2
        elif sentiment == 'neutral':
            risk_score += 1
        
        # Factor 4: Historical pattern (consecutive bad days)
        consecutive_bad = self._count_consecutive_bad_days(user_history)
        consecutive_threshold = self.burnout_thresholds.get('consecutive_bad_days', 3)
        if consecutive_bad >= consecutive_threshold:
            risk_score += 2
        
        # Map score to risk level
        if risk_score >= 5:
            return 'high'
        elif risk_score >= 3:
            return 'medium'
        else:
            return 'low'
    
    def _count_consecutive_bad_days(self, history: List) -> int:
        """Count consecutive days with negative indicators"""
        if not history:
            return 0
        
        consecutive = 0
        for day in reversed(history[-7:]):  # Check last 7 days
            if day.get('sentiment') == 'negative' or day.get('sleep_minutes', 420) < 360:
                consecutive += 1
            else:
                break
        
        return consecutive
    
    def _assess_sleep_quality(self, sleep_data: Dict) -> str:
        """Assess sleep quality: excellent, good, fair, poor"""
        minutes = sleep_data.get('minutes_asleep', 0)
        efficiency = sleep_data.get('efficiency', 0)
        
        if minutes >= 420 and efficiency >= 85:
            return 'excellent'
        elif minutes >= 360 and efficiency >= 75:
            return 'good'
        elif minutes >= 300:
            return 'fair'
        else:
            return 'poor'
    
    def _assess_activity(self, activity_data: Dict) -> str:
        """Assess activity level: high, moderate, low"""
        active_minutes = activity_data.get('active_minutes', 0)
        steps = activity_data.get('steps', 0)
        
        if active_minutes >= 60 or steps >= 10000:
            return 'high'
        elif active_minutes >= 30 or steps >= 5000:
            return 'moderate'
        else:
            return 'low'


class RecommendationAgent:
    """Agent for generating personalized micro-habits and mood playlists"""
    
    def __init__(self, config: Dict):
        self.config = config
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate personalized recommendations based on analysis
        
        Returns:
            dict: Micro-habits, playlist, and actionable suggestions
        """
        logger.info("Recommendation Agent: Generating recommendations...")
        
        analysis_data = task.get('analysis_data', {})
        
        # Generate context for habit recommendations
        context = {
            'sleep_quality': analysis_data.get('sleep_quality'),
            'activity_level': analysis_data.get('activity_level'),
            'burnout_risk': analysis_data.get('burnout_risk')
        }
        
        # Generate micro-habits
        habits = sentiment_analyzer.generate_micro_habits(
            sentiment=analysis_data.get('sentiment', 'neutral'),
            emotion=analysis_data.get('emotion', 'calm'),
            context=context
        )
        
        # Generate mood playlist
        playlist = None
        if task.get('spotify_enabled'):
            try:
                sp_client = task.get('spotify_client')
                playlist = SpotifyClient.create_mood_playlist(
                    mood=analysis_data.get('sentiment', 'neutral'),
                    emotion=analysis_data.get('emotion'),
                    sp_client=sp_client
                )
            except Exception as e:
                logger.warning(f"Spotify playlist creation failed: {e}, using mock")
                playlist = mock_mood_playlist(
                    analysis_data.get('sentiment', 'neutral'),
                    analysis_data.get('emotion')
                )
        else:
            playlist = mock_mood_playlist(
                analysis_data.get('sentiment', 'neutral'),
                analysis_data.get('emotion')
            )
        
        # Burnout-specific interventions
        interventions = self._generate_interventions(analysis_data.get('burnout_risk'))
        
        result = {
            'micro_habits': habits,
            'playlist': playlist,
            'interventions': interventions,
            'recommendation_timestamp': datetime.now().isoformat()
        }
        
        logger.info("Recommendation Agent: Recommendations generated")
        return result
    
    def _generate_interventions(self, burnout_risk: str) -> List[str]:
        """Generate risk-specific interventions"""
        interventions_map = {
            'high': [
                "⚠️ Consider scheduling a mental health check-in",
                "🛌 Prioritize 8+ hours of sleep tonight",
                "🧘 Try a 15-minute meditation or relaxation session",
                "💬 Reach out to a friend or counselor for support"
            ],
            'medium': [
                "⚡ Take regular breaks throughout your day",
                "🌳 Spend 20 minutes in nature if possible",
                "📵 Set boundaries with work/screen time"
            ],
            'low': [
                "✨ You're doing well! Keep up your healthy habits",
                "🎯 Set a small wellness goal for tomorrow"
            ]
        }
        
        return interventions_map.get(burnout_risk, interventions_map['low'])


class SynthesisAgent:
    """Agent for aggregating insights and personalizing based on user history"""
    
    def __init__(self, config: Dict):
        self.config = config
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesize all data into a personalized wellness report
        
        Returns:
            dict: Complete wellness insights with personalized messaging
        """
        logger.info("Synthesis Agent: Creating personalized report...")

        # Use `or {}` to guard against keys that exist but have value None
        ingestion_data = task.get('ingestion_data') or {}
        analysis_data = task.get('analysis_data') or {}
        recommendations = task.get('recommendations') or {}

        # Create personalized summary message
        summary = self._create_summary(ingestion_data, analysis_data)

        # Adapt recommendations based on user preferences/history
        adapted_habits = self._adapt_to_user_history(
            recommendations.get('micro_habits', []),
            task.get('user_preferences') or {}
        )

        # Generate trend insights if history available
        trends = self._analyze_trends(task.get('user_history') or [])

        # Compile final report
        report = {
            'success': True,
            'summary': summary,
            'sentiment': analysis_data.get('sentiment'),
            'emotion': analysis_data.get('emotion'),
            'burnout_risk': analysis_data.get('burnout_risk'),
            'sleep_quality': analysis_data.get('sleep_quality'),
            'activity_level': analysis_data.get('activity_level'),
            'micro_habits': adapted_habits,
            'interventions': recommendations.get('interventions', []),
            'playlist': recommendations.get('playlist'),
            'trends': trends,
            'data_summary': {
                'sleep_hours': round((ingestion_data.get('sleep') or {}).get('minutes_asleep', 0) / 60, 1),
                'steps': (ingestion_data.get('activity') or {}).get('steps', 0),
                'active_minutes': (ingestion_data.get('activity') or {}).get('active_minutes', 0),
                'calories': (ingestion_data.get('nutrition') or {}).get('calories', 'N/A')
            },
            'generated_at': datetime.now().isoformat()
        }
        
        logger.info("Synthesis Agent: Report complete")
        return report
    
    def _create_summary(self, ingestion_data: Dict, analysis_data: Dict) -> str:
        """Create a personalized summary message"""
        sentiment = analysis_data.get('sentiment', 'neutral')
        emotion = analysis_data.get('emotion', 'calm')
        sleep_quality = analysis_data.get('sleep_quality', 'unknown')
        burnout_risk = analysis_data.get('burnout_risk', 'low')
        
        # Sentiment-based greeting
        greetings = {
            'positive': f"Great to see you feeling {emotion}! ✨",
            'neutral': f"Thanks for checking in today. 🌟",
            'negative': f"I notice you're feeling {emotion}. Let's work on that together. 💙"
        }
        
        greeting = greetings.get(sentiment, "Welcome to your wellness check-in!")
        
        # Sleep feedback
        sleep_feedback = {
            'excellent': "Your sleep was excellent last night! 🌙",
            'good': "You got decent sleep. 😴",
            'fair': "Your sleep could use some improvement. 💤",
            'poor': "You're not getting enough rest. Let's prioritize sleep tonight. 🛌"
        }
        
        sleep_msg = sleep_feedback.get(sleep_quality, "")
        
        # Risk-aware messaging
        if burnout_risk == 'high':
            risk_msg = "I'm concerned about your burnout risk. Please take extra care of yourself today. ⚠️"
        elif burnout_risk == 'medium':
            risk_msg = "Your stress levels seem elevated. Let's focus on self-care. 🧘"
        else:
            risk_msg = "You're managing well! Keep it up. 💪"
        
        return f"{greeting} {sleep_msg} {risk_msg}"
    
    def _adapt_to_user_history(self, habits: List[str], preferences: Dict) -> List[str]:
        """Adapt habit recommendations based on user preferences and past compliance"""
        # Simple adaptation: filter out habits user has marked as "not helpful"
        disliked_keywords = preferences.get('disliked_activities', [])
        
        if not disliked_keywords:
            return habits
        
        adapted = []
        for habit in habits:
            if not any(keyword.lower() in habit.lower() for keyword in disliked_keywords):
                adapted.append(habit)
        
        return adapted if adapted else habits  # Return original if all filtered out
    
    def _analyze_trends(self, history: List[Dict]) -> Dict[str, Any]:
        """Analyze trends from user history"""
        if not history or len(history) < 3:
            return {'available': False, 'message': 'Not enough data for trend analysis'}
        
        # Calculate averages over last 7 days
        recent = history[-7:]
        
        avg_sleep = sum(day.get('sleep_minutes', 0) for day in recent) / len(recent)
        avg_sentiment_score = sum(
            1 if day.get('sentiment') == 'positive' else (-1 if day.get('sentiment') == 'negative' else 0)
            for day in recent
        ) / len(recent)
        
        return {
            'available': True,
            'avg_sleep_hours': round(avg_sleep / 60, 1),
            'mood_trend': 'improving' if avg_sentiment_score > 0 else ('declining' if avg_sentiment_score < 0 else 'stable'),
            'days_analyzed': len(recent)
        }


# Global orchestrator instance
def create_orchestrator(config_path: str = 'wellness_config.yaml') -> WellnessOrchestrator:
    """Factory function to create orchestrator instance"""
    return WellnessOrchestrator(config_path)
