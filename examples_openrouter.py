"""
Example: Using OpenRouter for Wellness Insights
Demonstrates the integration of OpenRouter API with AI models for wellness applications
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def example_basic_openrouter():
    """Example 1: Basic OpenRouter usage with OpenAI SDK"""
    print("="*70)
    print("Example 1: Basic OpenRouter Chat")
    print("="*70)
    
    client = OpenAI(
        api_key=os.environ.get('OPENROUTER_API_KEY'), 
        base_url="https://openrouter.ai/api/v1"
    )
    
    response = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful wellness assistant"},
            {"role": "user", "content": "What are 3 quick tips for better sleep?"},
        ],
        stream=False
    )
    
    print(response.choices[0].message.content)
    print()


def example_wellness_analysis():
    """Example 2: Wellness data analysis with OpenRouter"""
    print("="*70)
    print("Example 2: Wellness Data Analysis")
    print("="*70)
    
    client = OpenAI(
        api_key=os.environ.get('OPENROUTER_API_KEY'),
        base_url="https://openrouter.ai/api/v1"
    )
    
    # Simulate wellness data
    wellness_data = {
        'sleep_hours': 5.5,
        'sleep_quality': 'poor',
        'mood': 'stressed and anxious',
        'steps': 3000,
        'meals': ['coffee only - skipped breakfast']
    }
    
    prompt = f"""
    Analyze this wellness data and provide insights:
    
    Sleep: {wellness_data['sleep_hours']} hours ({wellness_data['sleep_quality']} quality)
    Mood: {wellness_data['mood']}
    Physical Activity: {wellness_data['steps']} steps today
    Nutrition: {', '.join(wellness_data['meals'])}
    
    Please provide:
    1. Overall wellness assessment
    2. Primary concerns
    3. Top 3 actionable recommendations (each 5-10 minutes)
    
    Be specific and practical.
    """
    
    response = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=[
            {"role": "system", "content": "You are an experienced wellness coach providing personalized health advice."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=400
    )
    
    print("📊 Wellness Analysis:")
    print(response.choices[0].message.content)
    print()


def example_sentiment_analysis():
    """Example 3: Mood sentiment analysis"""
    print("="*70)
    print("Example 3: Mood Sentiment Analysis")
    print("="*70)
    
    client = OpenAI(
        api_key=os.environ.get('OPENROUTER_API_KEY'),
        base_url="https://openrouter.ai/api/v1"
    )
    
    mood_entries = [
        "Feeling overwhelmed with work deadlines. Can't seem to focus.",
        "Great day! Went for a morning run and feel energized.",
        "Tired but productive. Getting things done slowly but surely."
    ]
    
    for i, entry in enumerate(mood_entries, 1):
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=[
                {"role": "system", "content": "Analyze the sentiment and emotion in this mood journal entry. Respond with: Sentiment (positive/neutral/negative), Primary Emotion, Brief Analysis."},
                {"role": "user", "content": entry},
            ],
            temperature=0.3,
            max_tokens=150
        )
        
        print(f"Entry {i}: \"{entry}\"")
        print(f"Analysis: {response.choices[0].message.content}")
        print()


def example_micro_habits():
    """Example 4: Generate personalized micro-habits"""
    print("="*70)
    print("Example 4: Personalized Micro-Habits Generation")
    print("="*70)
    
    client = OpenAI(
        api_key=os.environ.get('OPENROUTER_API_KEY'),
        base_url="https://openrouter.ai/api/v1"
    )
    
    user_context = {
        'burnout_risk': 'high',
        'sleep_quality': 'poor',
        'stress_level': 'high',
        'available_time': '5-10 minutes',
        'dislikes': ['meditation', 'yoga']
    }
    
    prompt = f"""
    Generate 3 personalized micro-habits for someone with:
    - Burnout Risk: {user_context['burnout_risk']}
    - Sleep Quality: {user_context['sleep_quality']}
    - Stress Level: {user_context['stress_level']}
    - Available Time: {user_context['available_time']}
    - Activities to Avoid: {', '.join(user_context['dislikes'])}
    
    Each habit should:
    - Take {user_context['available_time']}
    - Be specific and actionable
    - Address the user's issues
    - Be something they can do TODAY
    
    Format: [Habit Name]: [Specific action]
    """
    
    response = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a wellness coach specializing in micro-habits and behavior change."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.8,
        max_tokens=300
    )
    
    print("🎯 Personalized Micro-Habits:")
    print(response.choices[0].message.content)
    print()


def example_with_opendeepsearch():
    """Example 5: Using OpenDeepSearch with OpenRouter backend"""
    print("="*70)
    print("Example 5: OpenDeepSearch + OpenRouter Integration")
    print("="*70)
    
    try:
        from opendeepsearch import OpenDeepSearchAgent
        
        # Set up OpenRouter with the configured model
        os.environ['LITELLM_MODEL_ID'] = 'openrouter/deepseek/deepseek-chat'
        
        # Initialize OpenDeepSearch
        search_agent = OpenDeepSearchAgent(
            model_name="openrouter/deepseek/deepseek-chat",
            max_iterations=2
        )
        
        # Research a wellness topic
        query = "What does recent research say about the connection between sleep quality and mental health?"
        
        print(f"🔍 Researching: {query}")
        print("(This may take a moment as it searches and analyzes web content...)\n")
        
        result = search_agent.run(query)
        
        print("📚 Research Summary:")
        print(result)
        print()
        
    except ImportError:
        print("⚠️  OpenDeepSearch not installed.")
        print("Install with: pip install git+https://github.com/sentient-agi/OpenDeepSearch.git")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()


def example_multi_turn_conversation():
    """Example 6: Multi-turn wellness coaching conversation"""
    print("="*70)
    print("Example 6: Multi-Turn Wellness Coaching")
    print("="*70)
    
    client = OpenAI(
        api_key=os.environ.get('OPENROUTER_API_KEY'),
        base_url="https://openrouter.ai/api/v1"
    )
    
    # Simulate a conversation
    conversation = [
        {"role": "system", "content": "You are a supportive wellness coach. Keep responses concise and actionable."},
        {"role": "user", "content": "I've been feeling burned out lately."},
    ]
    
    # First response
    response1 = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=conversation,
        temperature=0.7,
        max_tokens=150
    )
    
    print("User: I've been feeling burned out lately.")
    print(f"Coach: {response1.choices[0].message.content}\n")
    
    # Add to conversation
    conversation.append({"role": "assistant", "content": response1.choices[0].message.content})
    conversation.append({"role": "user", "content": "I'm sleeping poorly and stressed about work."})
    
    # Second response
    response2 = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=conversation,
        temperature=0.7,
        max_tokens=200
    )
    
    print("User: I'm sleeping poorly and stressed about work.")
    print(f"Coach: {response2.choices[0].message.content}\n")


if __name__ == "__main__":
    print("\n🤖 OpenRouter Wellness Examples")
    print("="*70)
    print()
    
    # Check for API key
    if not os.environ.get('OPENROUTER_API_KEY'):
        print("❌ Error: OPENROUTER_API_KEY not found in environment")
        print("Please add it to your .env file:")
        print("OPENROUTER_API_KEY=sk-your-key-here")
        exit(1)
    
    try:
        # Run examples
        example_basic_openrouter()
        input("Press Enter to continue to next example...")
        
        example_wellness_analysis()
        input("Press Enter to continue to next example...")
        
        example_sentiment_analysis()
        input("Press Enter to continue to next example...")
        
        example_micro_habits()
        input("Press Enter to continue to next example...")
        
        example_multi_turn_conversation()
        input("Press Enter to continue to next example...")
        
        example_with_opendeepsearch()
        
        print("="*70)
        print("✅ All examples completed!")
        print("="*70)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Examples interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
