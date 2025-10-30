# 🧘 Wellness Oracle

**Your AI-Powered Personalized Health Coach with OpenRouter + Sentient's AGI Open Deep Search**

Wellness Oracle is an intelligent web application that analyzes your sleep, meals, and mood to provide hyper-personalized wellness recommendations. Powered by **OpenRouter** AI gateway and **Open Deep Search**, it integrates with Fitbit, Nutritionix, and Spotify to deliver comprehensive health insights with AI-driven analysis.

[![OpenRouter](https://img.shields.io/badge/OpenRouter-AI%20Gateway-purple)](https://openrouter.ai/)
[![OpenDeepSearch](https://img.shields.io/badge/OpenDeepSearch-Integrated-orange)](https://github.com/sentient-agi/OpenDeepSearch)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey)](https://flask.palletsprojects.com/)

---

## 🎯 AI-Powered with OpenRouter + Open Deep Search

This project uses **OpenRouter** as the AI gateway with **Open Deep Search** for enhanced capabilities:

- 🤖 **OpenRouter Gateway** - Unified access to multiple AI models (default: deepseek/deepseek-chat)
- 🧠 **Flexible Model Selection** - Easily switch between different AI models
- 🔍 **Open Deep Search** - Enhanced web search and context building
- 🔄 **OpenAI-Compatible** - Seamless integration using OpenAI SDK
- ⚡ **High Performance** - Fast inference with strong analytical capabilities
- 🎯 **Hierarchical Agents** - Modular wellness analysis workflow

---

## ✨ Features

- 📊 **Multi-Source Data Integration**
  - Fitbit API for sleep & activity tracking
  - Nutritionix for meal/nutrition analysis
  - Manual data entry fallback

- 🧠 **AI-Powered Analysis with OpenRouter**
  - **OpenRouter** gateway for advanced AI reasoning
  - **Open Deep Search** for context-aware insights
  - Sentiment analysis and emotion detection
  - Burnout risk prediction
  - Pattern recognition across historical data

- 🎯 **Personalized Recommendations**
  - Daily micro-habits (5-10 minute activities)
  - Context-aware wellness interventions
  - Adaptive suggestions based on user history
  - **Reasoning explanations** for each recommendation

- 🎵 **Mood-Based Playlists**
  - Automatic Spotify playlist generation
  - Emotion-to-music mapping
  - Personalized track selection

- 📈 **Wellness Trends**
  - Historical data visualization
  - Sleep quality tracking
  - Mood trend analysis

- 🤖 **Intelligent Orchestration**
  - Hierarchical agent workflow
  - Multi-phase analysis pipeline
  - Quality assessment of data inputs
  - Actionable recommendations

## 🏗️ Architecture

```
wellness-oracle/
├── app.py                  # Flask application entry point
├── config.py               # Configuration management
├── models.py               # SQLAlchemy database models
├── requirements.txt        # Python dependencies
├── wellness_config.yaml    # Wellness orchestrator configuration
│
├── agents/
│   ├── __init__.py
│   └── wellness.py         # Hierarchical wellness agents
│                           # - WellnessOrchestrator
│                           # - IngestionAgent
│                           # - AnalysisAgent
│                           # - RecommendationAgent
│                           # - SynthesisAgent
│
├── utils/
│   ├── __init__.py
│   ├── fitbit.py           # Fitbit API wrapper
│   ├── sentiment.py        # OpenRouter sentiment analysis
│   └── spotify.py          # Spotify API wrapper
│
└── templates/
    ├── base.html           # Base template with navigation
    ├── index.html          # Landing page
    ├── login.html          # Simple authentication
    ├── dashboard.html      # User dashboard
    ├── log.html            # Data entry form
    ├── insights.html       # Wellness insights display
    ├── oracle.html         # Chat interface
    └── history.html        # Historical data view
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip and virtualenv
- Git

### 1. Clone and Setup

```bash
# Create project directory
cd wellness

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (bash):
source venv/Scripts/activate
# On macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the template and fill in your API credentials:

```bash
cp .env.template .env
```

Edit `.env` with your API keys:

```env
# Required for full functionality
NUTRITIONIX_APP_ID=your_nutritionix_app_id
NUTRITIONIX_API_KEY=your_nutritionix_api_key

FITBIT_CLIENT_ID=your_fitbit_client_id
FITBIT_CLIENT_SECRET=your_fitbit_client_secret

SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret

OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=deepseek/deepseek-chat

# Generate a secure secret key
SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(16))')
```

### 3. Get API Credentials

#### Nutritionix (Meal Analysis)
1. Visit [developer.nutritionix.com](https://developer.nutritionix.com)
2. Sign up for a free account
3. Create an app to get **App ID** and **API Key**
4. Free tier: 1,000 requests/month

#### Fitbit (Wearable Data)
1. Visit [dev.fitbit.com](https://dev.fitbit.com)
2. Register your application
3. Set callback URL: `http://localhost:5000/fitbit/callback`
4. Get **Client ID** and **Client Secret**
5. Scopes needed: `activity`, `heartrate`, `sleep`, `profile`

#### Spotify (Mood Playlists)
1. Visit [developer.spotify.com](https://developer.spotify.com/dashboard)
2. Create an app
3. Set redirect URI: `http://localhost:5000/spotify/callback`
4. Get **Client ID** and **Client Secret**

#### OpenRouter (AI Gateway for Sentiment Analysis)
1. Visit [openrouter.ai](https://openrouter.ai)
2. Create an account and get an API key
3. Default model: `deepseek/deepseek-chat` (cost-effective)
4. Supports 200+ models - easily switchable via configuration

### 4. Run the Application

```bash
# Initialize database and start server
python app.py
```

Visit **http://localhost:5000** in your browser!

## 📖 Usage Guide

### First Time Setup

1. **Login/Register**: Enter any username (auto-creates account)
2. **Connect Integrations** (optional but recommended):
   - Click "Connect Fitbit" for automatic sleep/activity tracking
   - Click "Connect Spotify" for mood playlists

### Daily Workflow

1. **Log Your Day**
   - Navigate to "Log Data"
   - Enter your mood/feelings in the text area
   - Add meal description (optional)
   - Enter sleep hours manually or leave blank if using Fitbit

2. **Get Insights**
   - System analyzes your data through ROMA agents
   - Receive personalized wellness report with:
     - Sentiment & emotion analysis
     - Burnout risk assessment
     - 3 micro-habits to try
     - Mood-based Spotify playlist
     - Wellness interventions (if needed)

3. **Track Progress**
   - View dashboard for weekly overview
   - Check history for all past entries
   - Observe trends in sleep and mood

### Oracle Chat

Ask questions like:
- "How has my sleep been this week?"
- "What's my burnout risk?"
- "Give me tips for better sleep"

## 🤖 ROMA Intelligence

### What is ROMA?

**ROMA (Recursive Open Meta-Agent)** is a hierarchical AI framework that:
- Decomposes complex wellness analysis into specialized subtasks
- Uses **DSPy Chain-of-Thought** for explainable reasoning
- Provides confidence scores for recommendations
- Adapts based on context and user history

### DSPy-Powered Features

With ROMA integration, you get:

1. **Quality Assessment**: DSPy evaluates data completeness
2. **Analysis Summary**: Natural language explanation of your wellness state
3. **Reasoning Traces**: Understand WHY recommendations are made
4. **Priority Actions**: Top 3 actions ranked by importance
5. **Confidence Scores**: Know how confident the system is (0-100)

### Example ROMA Output

```python
{
    'summary': 'Great to see you feeling happy! Your sleep was excellent...',
    'dspy_insights': {
        'quality_assessment': 'High quality data - all sources available',
        'analysis_summary': 'User shows positive emotional state with excellent sleep quality...',
        'recommendation_reasoning': 'Recommendations focus on maintaining current wellness patterns...',
        'priority_actions': '1. Continue sleep routine\n2. Maintain activity level\n3. Practice gratitude',
        'confidence_score': '92'
    }
}
```

### ROMA Documentation

For detailed ROMA usage, see **[ROMA_GUIDE.md](ROMA_GUIDE.md)** which covers:
- DSPy signatures and modules
- Custom agent creation
- LLM model switching (GPT-3.5 vs GPT-4)
- Performance optimization
- Advanced customization

## 🔧 Configuration

### ROMA Orchestrator

Edit `roma_config.yaml` to customize:

```yaml
# Adjust processing depth
root_agent:
  max_depth: 3
  parallel_subtasks: true

# Configure burnout thresholds
tools:
  burnout_predictor:
    thresholds:
      sleep_minimum: 360  # minutes (6 hours)
      activity_minimum: 30  # minutes
      consecutive_bad_days: 3

# LLM model for DSPy reasoning
profiles:
  default: "gpt-3.5-turbo"  # Fast and cost-effective
  advanced: "gpt-4o-mini"   # Better reasoning
```

### Switch ROMA Models

Edit `app.py` to use different LLMs:

```python
# Use GPT-4 for better reasoning
orchestrator = ROMAWellnessOrchestrator(
    config_path='roma_config.yaml',
    model='gpt-4'  # or 'gpt-4o-mini', 'gpt-3.5-turbo'
)
```

### Scheduler Settings

Daily nudges sent at 8 AM. Modify in `app.py`:

```python
scheduler.add_job(
    func=send_daily_nudges,
    trigger='cron',
    hour=8,  # Change this
    minute=0
)
```

## 🧪 Testing

### Run Without API Keys

The app includes mock data generators:
- Works offline with simulated data
- Perfect for development/testing
- No API costs incurred

### Manual Testing

```bash
# Test individual components
python -c "from utils import nutrition_analyzer; print(nutrition_analyzer.analyze_meal('apple'))"
```

### Unit Tests (Future)

```bash
# When tests are added
pytest tests/
```

## 🗄️ Database

SQLite database (`users.db`) stores:
- User accounts & preferences
- Wellness log entries
- OAuth tokens (⚠️ encrypt in production!)

### Reset Database

```bash
# Delete and recreate
rm users.db
python app.py  # Auto-creates on startup
```

## 🔐 Security Notes

⚠️ **For Production Deployment:**

1. **Encrypt OAuth Tokens**: Current storage is plain text
2. **Use HTTPS**: Required for OAuth callbacks
3. **Secure SECRET_KEY**: Use environment variable
4. **Rate Limiting**: Add Flask-Limiter
5. **Input Validation**: Already basic, enhance as needed
6. **Authentication**: Current is session-based (username only)

## 🚀 Deployment

### Heroku Deployment

```bash
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Add gunicorn to requirements
pip install gunicorn
pip freeze > requirements.txt

# Deploy
heroku create wellness-oracle-app
git push heroku main
```

### Environment Variables

Set on hosting platform:
```bash
heroku config:set OPENAI_API_KEY=your_key
heroku config:set SECRET_KEY=your_secret
# ... etc
```

### Update Callback URLs

Update in API dashboards:
- Fitbit: `https://yourapp.herokuapp.com/fitbit/callback`
- Spotify: `https://yourapp.herokuapp.com/spotify/callback`

## 📊 ROMA Workflow

The Wellness Oracle uses a ROMA-inspired hierarchical workflow:

```
User Input
    ↓
┌─────────────────────────┐
│  Root Orchestrator      │
└───────────┬─────────────┘
            │
    ┌───────┴────────┐
    │                │
    ▼                ▼
┌─────────┐    ┌──────────┐
│Ingestion│    │ Analysis │
│  Agent  │───>│  Agent   │
└─────────┘    └────┬─────┘
                    │
            ┌───────┴────────┐
            │                │
            ▼                ▼
    ┌──────────────┐  ┌──────────┐
    │Recommendation│  │Synthesis │
    │    Agent     │─>│  Agent   │
    └──────────────┘  └────┬─────┘
                           │
                           ▼
                    Final Insights
```

Each agent is independent and can be modified/extended without affecting others.

## 🛠️ Customization

### Add New Data Sources

1. Create wrapper in `utils/new_source.py`
2. Add to `IngestionAgent` in `agents/wellness.py`
3. Update `roma_config.yaml`

### Custom Recommendation Logic

Edit `RecommendationAgent.execute()` in `agents/wellness.py`

### Extend Database

Add fields to models in `models.py`, then:
```bash
# In production, use migrations (Flask-Migrate)
# For now, drop and recreate:
rm users.db
python app.py
```

## 🐛 Troubleshooting

### "Import errors" when running
```bash
# Ensure virtual environment is activated
source venv/Scripts/activate  # Windows bash
pip install -r requirements.txt
```

### OAuth callbacks fail
- Check callback URLs match in API dashboards
- Ensure using `http://localhost:5000` (not 127.0.0.1)
- For Spotify, token expires - reconnect periodically

### No recommendations appearing
- Check API keys in `.env`
- View console logs for errors
- App falls back to mock data if APIs fail

### Database locked errors
```bash
# Close all connections and restart
rm users.db
python app.py
```

## 📚 API Documentation

### Nutritionix
- Docs: https://docs.nutritionix.com
- Endpoints used: `/v2/natural/nutrients`

### Fitbit
- Docs: https://dev.fitbit.com/build/reference/web-api/
- Endpoints used: `/sleep`, `/activities`

### OpenAI
- Docs: https://platform.openai.com/docs
- Model: `gpt-3.5-turbo`

### Spotify
- Docs: https://developer.spotify.com/documentation/web-api
- Endpoints used: `/recommendations`, `/playlists`

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Add pytest unit tests
- [ ] Implement proper authentication (JWT/OAuth)
- [ ] Add data visualization charts
- [ ] Email/SMS notifications for nudges
- [ ] Mobile responsive improvements
- [ ] Export data to CSV/PDF
- [ ] Integration with Apple Health
- [ ] Machine learning for better burnout prediction

## 📄 License

MIT License - feel free to use and modify for your projects!

## 🙏 Acknowledgments

- **ROMA Framework**: Recursive Open Meta-Agent concept
- **Flask**: Web framework
- **OpenAI**: Sentiment analysis
- **Fitbit, Nutritionix, Spotify**: Data APIs

## 📧 Support

For questions or issues:
1. Check the troubleshooting section above
2. Review API documentation links
3. Check console logs for specific errors

---

**Built with ❤️ for better wellness through AI**

MVP Build Time: ~2 weeks | Last Updated: October 2025


