"""
Spotify API integration for mood-based playlist generation
"""
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import Config
import logging

logger = logging.getLogger(__name__)


class SpotifyClient:
    """Wrapper for Spotify API with mood-based recommendations"""
    
    @staticmethod
    def get_auth_manager():
        """Get Spotify OAuth2 manager"""
        return SpotifyOAuth(
            client_id=Config.SPOTIFY_CLIENT_ID,
            client_secret=Config.SPOTIFY_CLIENT_SECRET,
            redirect_uri=Config.SPOTIFY_REDIRECT_URI,
            scope="playlist-modify-public playlist-modify-private user-library-read"
        )
    
    @staticmethod
    def get_client(access_token: str = None):
        """
        Get authenticated Spotify client
        
        Args:
            access_token: OAuth2 access token
            
        Returns:
            spotipy.Spotify: Authenticated Spotify client
        """
        if access_token:
            return spotipy.Spotify(auth=access_token)
        else:
            auth_manager = SpotifyClient.get_auth_manager()
            return spotipy.Spotify(auth_manager=auth_manager)
    
    @staticmethod
    def create_mood_playlist(
        mood: str,
        emotion: str = None,
        sp_client: spotipy.Spotify = None,
        playlist_name: str = None,
        limit: int = 15
    ) -> dict:
        """
        Create a mood-based playlist
        
        Args:
            mood: Sentiment (positive, neutral, negative)
            emotion: Specific emotion keyword
            sp_client: Authenticated Spotify client
            playlist_name: Custom playlist name
            limit: Number of tracks to include
            
        Returns:
            dict: Playlist info with URL
        """
        if not sp_client:
            try:
                sp_client = SpotifyClient.get_client()
            except Exception as e:
                logger.error(f"Failed to authenticate with Spotify: {str(e)}")
                return {'success': False, 'error': 'Spotify authentication failed'}
        
        try:
            # Map mood/emotion to Spotify recommendation parameters
            mood_params = SpotifyClient._get_mood_parameters(mood, emotion)
            
            # Get recommendations
            recommendations = sp_client.recommendations(
                seed_genres=mood_params['genres'],
                limit=limit,
                target_energy=mood_params['energy'],
                target_valence=mood_params['valence'],
                target_tempo=mood_params['tempo']
            )
            
            if not recommendations.get('tracks'):
                return {'success': False, 'error': 'No recommendations found'}
            
            # Create playlist
            user_id = sp_client.current_user()['id']
            
            if not playlist_name:
                playlist_name = f"Wellness Boost - {emotion.title() if emotion else mood.title()}"
            
            playlist = sp_client.user_playlist_create(
                user_id,
                playlist_name,
                public=False,
                description=f"Personalized wellness playlist for {emotion or mood} mood"
            )
            
            # Add tracks
            track_uris = [track['uri'] for track in recommendations['tracks']]
            sp_client.playlist_add_items(playlist['id'], track_uris)
            
            return {
                'success': True,
                'playlist_url': playlist['external_urls']['spotify'],
                'playlist_id': playlist['id'],
                'playlist_name': playlist_name,
                'track_count': len(track_uris),
                'tracks': [
                    {
                        'name': t['name'],
                        'artist': t['artists'][0]['name'],
                        'url': t['external_urls']['spotify']
                    }
                    for t in recommendations['tracks'][:5]  # First 5 tracks
                ]
            }
            
        except Exception as e:
            logger.error(f"Error creating mood playlist: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def _get_mood_parameters(mood: str, emotion: str = None) -> dict:
        """
        Map mood/emotion to Spotify audio features
        
        Spotify parameters:
        - energy: 0.0 to 1.0 (calm to energetic)
        - valence: 0.0 to 1.0 (sad to happy)
        - tempo: BPM (beats per minute)
        """
        # Default mood mappings
        mood_map = {
            'positive': {
                'genres': ['pop', 'indie-pop', 'happy'],
                'energy': 0.7,
                'valence': 0.8,
                'tempo': 120
            },
            'neutral': {
                'genres': ['chill', 'indie', 'acoustic'],
                'energy': 0.5,
                'valence': 0.5,
                'tempo': 100
            },
            'negative': {
                'genres': ['acoustic', 'ambient', 'piano'],
                'energy': 0.3,
                'valence': 0.3,
                'tempo': 80
            }
        }
        
        # Emotion-specific adjustments
        emotion_adjustments = {
            'anxious': {'genres': ['ambient', 'classical', 'meditation'], 'energy': 0.2, 'valence': 0.4, 'tempo': 60},
            'stressed': {'genres': ['acoustic', 'chill', 'ambient'], 'energy': 0.3, 'valence': 0.4, 'tempo': 75},
            'excited': {'genres': ['dance', 'pop', 'electronic'], 'energy': 0.9, 'valence': 0.9, 'tempo': 130},
            'sad': {'genres': ['acoustic', 'piano', 'singer-songwriter'], 'energy': 0.3, 'valence': 0.3, 'tempo': 70},
            'happy': {'genres': ['pop', 'dance', 'happy'], 'energy': 0.8, 'valence': 0.9, 'tempo': 125},
            'calm': {'genres': ['ambient', 'chill', 'classical'], 'energy': 0.4, 'valence': 0.6, 'tempo': 90},
            'energetic': {'genres': ['workout', 'rock', 'electronic'], 'energy': 0.9, 'valence': 0.7, 'tempo': 140}
        }
        
        # Use emotion-specific parameters if available, otherwise use mood
        if emotion and emotion.lower() in emotion_adjustments:
            return emotion_adjustments[emotion.lower()]
        
        return mood_map.get(mood.lower(), mood_map['neutral'])
    
    @staticmethod
    def get_user_top_tracks(sp_client: spotipy.Spotify = None, limit: int = 10, time_range: str = 'short_term') -> list:
        """
        Get user's top tracks for personalization
        
        Args:
            sp_client: Authenticated Spotify client
            limit: Number of tracks
            time_range: 'short_term', 'medium_term', or 'long_term'
            
        Returns:
            list: Top tracks
        """
        if not sp_client:
            sp_client = SpotifyClient.get_client()
        
        try:
            results = sp_client.current_user_top_tracks(limit=limit, time_range=time_range)
            return [
                {
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'id': track['id']
                }
                for track in results['items']
            ]
        except Exception as e:
            logger.error(f"Error fetching top tracks: {str(e)}")
            return []


# Mock playlist generator
def mock_mood_playlist(mood: str, emotion: str = None) -> dict:
    """Generate mock playlist data for testing"""
    return {
        'success': True,
        'playlist_url': f'https://open.spotify.com/playlist/mock_{mood}_{emotion}',
        'playlist_name': f'Wellness Boost - {emotion.title() if emotion else mood.title()}',
        'track_count': 15,
        'tracks': [
            {'name': 'Sample Track 1', 'artist': 'Artist A', 'url': 'https://open.spotify.com/track/1'},
            {'name': 'Sample Track 2', 'artist': 'Artist B', 'url': 'https://open.spotify.com/track/2'},
            {'name': 'Sample Track 3', 'artist': 'Artist C', 'url': 'https://open.spotify.com/track/3'}
        ],
        'mock': True
    }
