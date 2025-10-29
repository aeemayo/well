"""
OpenRouter API integration for sentiment analysis and emotional intelligence
"""
from openai import OpenAI
from config import Config
import logging

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """AI-powered sentiment analysis using OpenRouter"""
    
    def __init__(self):
        if not Config.OPENROUTER_API_KEY:
            logger.warning("OpenRouter API key not configured")
            self.client = None
        else:
            self.client = OpenAI(
                api_key=Config.OPENROUTER_API_KEY,
                base_url=Config.OPENROUTER_BASE_URL
            )
    
    def analyze_sentiment(self, text: str) -> dict:
        """
        Analyze sentiment of text using GPT
        
        Args:
            text: Text to analyze (mood note, journal entry, etc.)
            
        Returns:
            dict: Sentiment classification and confidence score
        """
        if not self.client:
            logger.warning("Using mock sentiment analysis")
            return self._mock_analysis(text)
        
        try:
            response = self.client.chat.completions.create(
                model=Config.OPENROUTER_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a sentiment analysis expert. Classify the sentiment as 'positive', 'neutral', or 'negative'. Also provide a brief emotion keyword (e.g., happy, anxious, calm, stressed)."
                    },
                    {
                        "role": "user",
                        "content": f"Classify the sentiment and identify the primary emotion in this text: '{text}'"
                    }
                ],
                max_tokens=50,
                temperature=0.3
            )
            
            result = response.choices[0].message.content.lower()
            
            # Parse the response
            sentiment = 'neutral'
            if 'positive' in result:
                sentiment = 'positive'
            elif 'negative' in result:
                sentiment = 'negative'
            
            # Extract emotion keyword
            emotion_keywords = ['happy', 'sad', 'anxious', 'calm', 'stressed', 'excited', 'worried', 'content', 'frustrated', 'energetic']
            emotion = 'neutral'
            for keyword in emotion_keywords:
                if keyword in result:
                    emotion = keyword
                    break
            
            return {
                'sentiment': sentiment,
                'emotion': emotion,
                'raw_response': result,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def generate_micro_habits(self, sentiment: str, emotion: str, context: dict = None) -> list:
        """
        Generate personalized micro-habits based on sentiment and context
        
        Args:
            sentiment: positive, neutral, or negative
            emotion: Specific emotion keyword
            context: Additional context (sleep quality, activity level, etc.)
            
        Returns:
            list: Micro-habit recommendations
        """
        if not self.client:
            return self._mock_habits(sentiment, emotion)
        
        try:
            context_str = ""
            if context:
                context_str = f"\nContext: Sleep quality: {context.get('sleep_quality', 'unknown')}, Activity level: {context.get('activity_level', 'unknown')}"
            
            response = self.client.chat.completions.create(
                model=Config.OPENROUTER_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a wellness coach. Suggest 3 specific, actionable micro-habits (5-10 minutes each) based on the person's emotional state."
                    },
                    {
                        "role": "user",
                        "content": f"Sentiment: {sentiment}, Emotion: {emotion}{context_str}\n\nSuggest 3 micro-habits:"
                    }
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            habits_text = response.choices[0].message.content
            # Split into individual habits
            habits = [h.strip() for h in habits_text.split('\n') if h.strip() and (h.strip()[0].isdigit() or h.strip().startswith('-'))]
            
            return habits[:3] if len(habits) >= 3 else habits
            
        except Exception as e:
            logger.error(f"Error generating habits: {str(e)}")
            return self._mock_habits(sentiment, emotion)
    
    def _mock_analysis(self, text: str) -> dict:
        """Mock sentiment analysis for testing"""
        # Simple keyword-based mock
        text_lower = text.lower()
        
        positive_words = ['good', 'great', 'happy', 'excellent', 'wonderful', 'love', 'joy']
        negative_words = ['bad', 'sad', 'angry', 'terrible', 'hate', 'stress', 'anxious', 'worry']
        
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            sentiment = 'positive'
            emotion = 'happy'
        elif neg_count > pos_count:
            sentiment = 'negative'
            emotion = 'stressed'
        else:
            sentiment = 'neutral'
            emotion = 'calm'
        
        return {
            'sentiment': sentiment,
            'emotion': emotion,
            'success': True,
            'mock': True
        }
    
    def _mock_habits(self, sentiment: str, emotion: str) -> list:
        """Mock habit recommendations"""
        habits_map = {
            'negative': [
                "Take 5 deep breaths focusing on slow exhales",
                "Write down 3 things you're grateful for today",
                "Step outside for a 10-minute walk in fresh air"
            ],
            'neutral': [
                "Do a 5-minute stretching routine",
                "Drink a glass of water mindfully",
                "Listen to your favorite uplifting song"
            ],
            'positive': [
                "Share your positive energy - call a friend",
                "Journal about what made today great",
                "Plan a small reward for yourself this week"
            ]
        }
        return habits_map.get(sentiment, habits_map['neutral'])


# Singleton instance
sentiment_analyzer = SentimentAnalyzer()
