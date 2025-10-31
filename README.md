# 🧘 Wellness Oracle

**Your AI-Powered Personalized Health Coach with OpenRouter + Open Deep Search**

Wellness Oracle is an intelligent web application that analyzes your sleep, meals, and mood to provide hyper-personalized wellness recommendations. Powered by **OpenRouter** AI gateway and **Open Deep Search**, it integrates with Fitbit, Nutritionix, and Spotify to deliver comprehensive health insights with AI-driven analysis.

[![OpenRouter](https://img.shields.io/badge/OpenRouter-AI%20Gateway-purple)](https://openrouter.ai/)
[![OpenDeepSearch](https://img.shields.io/badge/OpenDeepSearch-Integrated-orange)](https://github.com/sentient-agi/OpenDeepSearch)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey)](https://flask.palletsprojects.com/)

---

## 🎯 AI-Powered with OpenRouter + OpenDeepSearch

This project leverages **OpenRouter** AI gateway and **OpenDeepSearch** for advanced wellness intelligence:

### 🔍 OpenDeepSearch Integration

**OpenDeepSearch** is an advanced AI-powered search and research framework that enhances wellness recommendations:

- 🌐 **Real-Time Web Research** - Searches and synthesizes latest wellness research, health trends, and evidence-based practices
- 🧠 **Context-Aware Analysis** - Builds comprehensive context about health topics, supplements, exercises, and interventions
- 📊 **Multi-Source Synthesis** - Aggregates information from medical journals, fitness blogs, nutrition databases, and health forums
- 🎯 **Intelligent Query Generation** - Automatically formulates research questions based on user's wellness patterns
- ⚡ **Rapid Knowledge Retrieval** - Quickly finds relevant health information to support personalized recommendations
- 🔬 **Evidence-Based Insights** - Cross-references multiple sources to provide scientifically-backed wellness advice

### 🤖 OpenRouter AI Gateway

- 🔄 **Multi-Model Support** - Access 200+ AI models through a unified API (default: deepseek/deepseek-chat)
- 💰 **Cost-Effective** - Choose the right model for your needs and budget
- � **OpenAI-Compatible** - Drop-in replacement using OpenAI SDK
- ⚡ **High Performance** - Fast inference with powerful reasoning capabilities

---

## ✨ Features

- 📊 **Multi-Source Data Integration**
  - Fitbit API for sleep & activity tracking
  - Nutritionix for meal/nutrition analysis
  - Manual data entry fallback

- 🧠 **AI-Powered Analysis with OpenRouter + OpenDeepSearch**
  - **OpenRouter** gateway for advanced AI reasoning
  - **OpenDeepSearch** for real-time wellness research and context building
  - Evidence-based recommendations backed by latest health research
  - Sentiment analysis and emotion detection
  - Burnout risk prediction
  - Pattern recognition across historical data
  - Automatic research on relevant health topics and interventions

- 🎯 **Personalized Recommendations**
  - Daily micro-habits (5-10 minute activities)
  - Context-aware wellness interventions powered by OpenDeepSearch
  - Adaptive suggestions based on user history
  - **Evidence-based reasoning** for each recommendation with research citations
  - Real-time research on emerging wellness trends and practices

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

## 🔍 Why OpenDeepSearch?

Traditional wellness apps rely on static databases and pre-programmed logic. **OpenDeepSearch transforms this by:**

1. **🌐 Real-Time Research** - Instead of static recommendations, the app searches current health literature when you log data
2. **📊 Evidence-Based Advice** - Every suggestion is backed by research papers, expert blogs, and credible health sources
3. **🎯 Personalized Context** - Searches specifically for information relevant to YOUR patterns and needs
4. **🔄 Always Current** - Recommendations stay up-to-date with latest wellness science and trends
5. **🔬 Source Transparency** - See where recommendations come from with citations and references
6. **🧠 Deep Understanding** - Synthesizes multiple sources to provide comprehensive, nuanced advice

**Example:** Instead of a generic "get more sleep" recommendation, OpenDeepSearch might find:
- Peer-reviewed research on your specific sleep duration needs
- Evidence-based techniques for your sleep issues (e.g., difficulty falling asleep vs. waking up)
- Recent studies on sleep hygiene practices that actually work
- Expert opinions on supplements, lighting, temperature, and routine optimizations

This makes every recommendation **personalized**, **current**, and **trustworthy**.

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
│   ├── nutrition.py        # Nutritionix API wrapper
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

**Note:** OpenDeepSearch is installed automatically from the GitHub repository via `requirements.txt`:
```
git+https://github.com/sentient-agi/OpenDeepSearch.git
```

### Verify OpenDeepSearch Installation

```bash
# Test OpenDeepSearch import
python -c "import opendeepsearch; print('OpenDeepSearch installed successfully!')"

# Check installed version
pip show opendeepsearch
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

### Oracle Chat (OpenDeepSearch-Powered)

Ask questions and get research-backed answers:
- "How has my sleep been this week?" - Includes latest sleep research
- "What's my burnout risk?" - Compares to evidence-based burnout indicators
- "Give me tips for better sleep" - Provides scientifically-validated sleep hygiene practices
- "What are the benefits of morning sunlight?" - Real-time research synthesis
- "Should I try meditation for stress?" - Evidence from multiple sources

**Behind the scenes:** OpenDeepSearch searches the web for relevant health information and synthesizes findings to support each answer with credible sources.

## 🔬 OpenDeepSearch Intelligence

### What is OpenDeepSearch?

**OpenDeepSearch** is an advanced AI-powered research framework that enhances wellness recommendations with real-time web research and synthesis:

- 🌐 **Autonomous Research Agent** - Automatically searches the web for relevant wellness information
- 🔍 **Smart Crawling** - Efficiently scrapes and processes health-related content from multiple sources
- 🧠 **Context Building** - Synthesizes information into coherent, actionable insights
- 📚 **Knowledge Aggregation** - Combines findings from medical journals, health blogs, nutrition databases, and forums
- 🎯 **Query Optimization** - Generates intelligent search queries based on your wellness patterns

### OpenDeepSearch-Powered Features

With OpenDeepSearch integration, the Wellness Oracle provides:

1. **Evidence-Based Recommendations** - All suggestions backed by real research and health literature
2. **Real-Time Health Insights** - Access to latest wellness trends, studies, and best practices
3. **Comprehensive Context** - Deep understanding of health topics relevant to your situation
4. **Source Citations** - Know where recommendations come from with credible references
5. **Adaptive Learning** - Continuously improves by researching new health information

### Example OpenDeepSearch Output

```python
{
    'recommendation': 'Try 10 minutes of morning sunlight exposure',
    'research_context': {
        'sources_found': 12,
        'key_findings': [
            'Morning sunlight regulates circadian rhythm (Sleep Medicine Reviews, 2024)',
            'Blue light exposure before 10am improves mood and alertness',
            'Vitamin D synthesis occurs within 10-15 minutes of sun exposure'
        ],
        'evidence_strength': 'High (meta-analysis of 23 studies)',
        'related_topics': ['circadian rhythm', 'vitamin D', 'mood regulation', 'sleep quality']
    },
    'reasoning': 'Based on your poor sleep quality and low mood, research indicates...'
}
```

### OpenDeepSearch Use Cases

The Wellness Oracle uses OpenDeepSearch to:

1. **Research Sleep Solutions** - When you report poor sleep, it searches for evidence-based sleep hygiene practices
2. **Investigate Nutrition** - Finds information about meals you logged, including nutritional benefits and concerns
3. **Discover Wellness Interventions** - Researches activities, supplements, and practices that match your needs
4. **Validate Recommendations** - Cross-references suggestions with medical literature and expert opinions
5. **Track Health Trends** - Monitors emerging wellness research and practices
6. **Personalize Advice** - Combines research with your specific patterns for targeted recommendations

## 🔧 Configuration

### Wellness Orchestrator with OpenDeepSearch

Edit `wellness_config.yaml` to customize:

```yaml
# OpenRouter Configuration
openrouter:
  api_key: ${OPENROUTER_API_KEY}
  base_url: "https://openrouter.ai/api/v1"
  model: "deepseek/deepseek-chat"  # Fast and cost-effective
  # Available models: "anthropic/claude-3.5-sonnet", "openai/gpt-4", etc.

# OpenDeepSearch Configuration
opendeepsearch:
  enabled: true
  max_results: 10  # Number of search results to process
  depth: "medium"  # shallow, medium, deep
  sources:
    - medical_journals
    - health_blogs
    - nutrition_databases
    - wellness_forums
  
# Burnout thresholds
burnout:
  sleep_minimum: 360  # minutes (6 hours)
  activity_minimum: 30  # minutes
  consecutive_bad_days: 3
  
# Recommendation settings
recommendations:
  count: 3  # Number of micro-habits to suggest
  duration: 10  # Maximum minutes per activity
  research_backed: true  # Require OpenDeepSearch validation
```

### Switch OpenRouter Models

Edit `wellness_config.yaml` or set environment variable:

```bash
# Use a more powerful model for complex reasoning
export OPENROUTER_MODEL="anthropic/claude-3.5-sonnet"

# Or use GPT-4 for better analysis
export OPENROUTER_MODEL="openai/gpt-4-turbo"

# Or stick with cost-effective DeepSeek
export OPENROUTER_MODEL="deepseek/deepseek-chat"
```

### Configure OpenDeepSearch Behavior

Control how deep the research goes:

```python
# In wellness_config.yaml
opendeepsearch:
  depth: "deep"  # More thorough research (slower but more comprehensive)
  max_results: 20  # Process more sources
  include_academic: true  # Include PubMed and research papers
  cache_results: true  # Cache research to avoid re-searching
  freshness: "1week"  # Only include recent findings
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

## 📊 Wellness Analysis Workflow with OpenDeepSearch

The Wellness Oracle uses an intelligent, research-augmented workflow:

```
User Input (Mood, Sleep, Meals)
    ↓
┌─────────────────────────────┐
│  Wellness Orchestrator      │
│  (OpenRouter + DeepSeek)    │
└──────────┬──────────────────┘
           │
    ┌──────┴─────────┐
    │                │
    ▼                ▼
┌──────────┐    ┌────────────────┐
│Data      │    │ OpenDeepSearch │
│Ingestion │    │ Research Agent │
└────┬─────┘    └───────┬────────┘
     │                  │
     │  ┌───────────────┘
     │  │ (Web research on relevant topics)
     ▼  ▼
┌──────────────────┐
│ Analysis Agent   │
│ (Sentiment, Risk)│
└────────┬─────────┘
         │
         ▼
┌──────────────────────────┐
│ Recommendation Agent     │
│ (Evidence-based habits)  │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Synthesis + Citations    │
│ (Final insights + refs)  │
└────────┬─────────────────┘
         │
         ▼
  Personalized Report
  with Research Backing
```

**Key Innovation:** OpenDeepSearch runs in parallel with analysis, researching relevant health topics to ensure all recommendations are evidence-based and current.

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

### OpenDeepSearch taking too long
- Reduce `max_results` in `wellness_config.yaml`
- Change `depth` from "deep" to "medium" or "shallow"
- Enable result caching: `cache_results: true`
- Check your internet connection

### OpenDeepSearch not finding relevant sources
- Ensure you have an active internet connection
- Check if specific domains are blocked by your network
- Try increasing `max_results` for broader search
- Review console logs for crawling errors

### Database locked errors
```bash
# Close all connections and restart
rm users.db
python app.py
```

## 📚 API Documentation

### OpenDeepSearch
- GitHub: https://github.com/sentient-agi/OpenDeepSearch
- Advanced AI-powered research and web crawling framework
- Provides real-time context building and synthesis

### OpenRouter
- Docs: https://openrouter.ai/docs
- AI gateway supporting 200+ models
- OpenAI-compatible API
- Default model: `deepseek/deepseek-chat`

### Nutritionix
- Docs: https://docs.nutritionix.com
- Endpoints used: `/v2/natural/nutrients`

### Fitbit
- Docs: https://dev.fitbit.com/build/reference/web-api/
- Endpoints used: `/sleep`, `/activities`

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
- [ ] Enhance OpenDeepSearch with more specialized health sources
- [ ] Cache OpenDeepSearch results for faster recommendations
- [ ] Add research confidence scores to recommendations

## 📄 License

MIT License - feel free to use and modify for your projects!

## 🙏 Acknowledgments

- **OpenDeepSearch**: Advanced AI-powered research framework by [Sentient AGI](https://github.com/sentient-agi/OpenDeepSearch)
- **OpenRouter**: AI gateway providing access to 200+ models
- **DeepSeek**: Cost-effective, powerful AI model for reasoning
- **Flask**: Web framework
- **Fitbit, Nutritionix, Spotify**: Data APIs

## 📧 Support

For questions or issues:
1. Check the troubleshooting section above
2. Review API documentation links
3. Check console logs for specific errors

---

**Built with ❤️ for better wellness through AI**

MVP Build Time: ~2 weeks | Last Updated: October 2025
