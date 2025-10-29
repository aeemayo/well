"""
Nutritionix API integration for meal and nutrition analysis
"""
from nutritionix import Nutritionix
from config import Config
import logging

logger = logging.getLogger(__name__)


class NutritionAnalyzer:
    """Wrapper for Nutritionix API"""
    
    def __init__(self):
        if not Config.NUTRITIONIX_APP_ID or not Config.NUTRITIONIX_API_KEY:
            logger.warning("Nutritionix credentials not configured")
            self.client = None
        else:
            self.client = Nutritionix(
                app_id=Config.NUTRITIONIX_APP_ID,
                api_key=Config.NUTRITIONIX_API_KEY
            )
    
    def analyze_meal(self, description: str) -> dict:
        """
        Analyze a meal description using natural language
        
        Args:
            description: Natural language meal description (e.g., "apple and banana")
            
        Returns:
            dict: Nutrition information including calories, protein, carbs, fat
        """
        if not self.client:
            logger.error("Nutritionix client not initialized")
            return self._mock_response(description)
        
        try:
            response = self.client.natural(
                query=description,
                fields=['nf_calories', 'nf_protein', 'nf_total_carbohydrate', 'nf_total_fat']
            )
            
            if response.get('foods') and len(response['foods']) > 0:
                food = response['foods'][0]
                return {
                    'food_name': food.get('food_name', description),
                    'calories': food.get('nf_calories', 0),
                    'protein': food.get('nf_protein', 0),
                    'carbs': food.get('nf_total_carbohydrate', 0),
                    'fat': food.get('nf_total_fat', 0),
                    'success': True
                }
            else:
                return {'success': False, 'error': 'No food data found'}
                
        except Exception as e:
            logger.error(f"Error analyzing meal: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _mock_response(self, description: str) -> dict:
        """Mock response for testing without API credentials"""
        return {
            'food_name': description,
            'calories': 150,
            'protein': 5,
            'carbs': 30,
            'fat': 2,
            'success': True,
            'mock': True
        }


# Singleton instance
nutrition_analyzer = NutritionAnalyzer()
