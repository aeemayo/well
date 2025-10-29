"""
Test OpenRouter Integration with OpenAI-Compatible Interface
Tests the OpenRouter API using OpenAI SDK binding
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openrouter_basic():
    """Test basic OpenRouter chat completion"""
    print("🧪 Testing OpenRouter with OpenAI Binding")
    print("="*70)
    
    # Check API key
    api_key = os.environ.get('OPENROUTER_API_KEY')
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in environment variables")
        print("   Please add it to your .env file:")
        print("   OPENROUTER_API_KEY=your_api_key_here")
        return False
    
    print(f"✅ API Key found: {api_key[:8]}...")
    
    try:
        # Initialize OpenAI client with OpenRouter endpoint
        client = OpenAI(
            api_key=api_key, 
            base_url="https://openrouter.ai/api/v1"
        )
        
        print("\n📡 Sending test request to OpenRouter API...")
        
        # Test request
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Hello! Please respond with 'OpenRouter is working!' if you can hear me."},
            ],
            stream=False
        )
        
        result = response.choices[0].message.content
        print(f"✅ Response received: {result}")
        
        # Print usage stats
        if hasattr(response, 'usage'):
            print(f"\n📊 Usage Statistics:")
            print(f"   Prompt tokens: {response.usage.prompt_tokens}")
            print(f"   Completion tokens: {response.usage.completion_tokens}")
            print(f"   Total tokens: {response.usage.total_tokens}")
        
        print("\n✅ OpenRouter integration test PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ OpenRouter integration test FAILED!")
        print(f"   Error: {str(e)}")
        return False


def test_openrouter_wellness_use_case():
    """Test OpenRouter with a wellness-related query"""
    print("\n\n🏥 Testing OpenRouter with Wellness Use Case")
    print("="*70)
    
    api_key = os.environ.get('OPENROUTER_API_KEY')
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found")
        return False
    
    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        
        print("\n📡 Sending wellness analysis request...")
        
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a wellness coach providing personalized health advice."},
                {"role": "user", "content": """
                Analyze this wellness data and provide insights:
                - Sleep: 5.5 hours (poor quality)
                - Mood: Feeling stressed and anxious
                - Activity: Only 3000 steps today
                - Nutrition: Skipped breakfast, only had coffee
                
                Provide 3 brief actionable recommendations.
                """},
            ],
            stream=False,
            temperature=0.7,
            max_tokens=300
        )
        
        result = response.choices[0].message.content
        print(f"✅ Wellness Analysis Response:\n{result}")
        
        print("\n✅ Wellness use case test PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ Wellness use case test FAILED!")
        print(f"   Error: {str(e)}")
        return False


def test_opendeepsearch_integration():
    """Test OpenDeepSearch with OpenRouter backend"""
    print("\n\n🔍 Testing OpenDeepSearch with OpenRouter Backend")
    print("="*70)
    
    try:
        from opendeepsearch import OpenDeepSearchAgent
        
        api_key = os.environ.get('OPENROUTER_API_KEY')
        if not api_key:
            print("❌ OPENROUTER_API_KEY not found")
            return False
        
        print("\n📦 OpenDeepSearch package imported successfully")
        print("📡 Initializing OpenDeepSearch with OpenRouter model...")
        
        # Note: OpenDeepSearch uses litellm internally
        # We need to set the model to use OpenRouter
        os.environ['LITELLM_MODEL_ID'] = 'openrouter/deepseek/deepseek-chat'
        os.environ['OPENROUTER_API_KEY'] = api_key
        
        # Initialize OpenDeepSearch
        search_agent = OpenDeepSearchAgent(
            model_name="openrouter/deepseek/deepseek-chat",
            max_iterations=3
        )
        
        print("✅ OpenDeepSearch initialized with OpenRouter backend")
        
        # Test a simple query
        print("\n📡 Running test search query...")
        result = search_agent.run(
            "What are the health benefits of good sleep?"
        )
        
        print(f"✅ Search completed!")
        print(f"   Result preview: {str(result)[:200]}...")
        
        print("\n✅ OpenDeepSearch integration test PASSED!")
        return True
        
    except ImportError as e:
        print(f"❌ OpenDeepSearch not installed: {e}")
        print("   Install with: pip install git+https://github.com/sentient-agi/OpenDeepSearch.git")
        return False
    except Exception as e:
        print(f"\n❌ OpenDeepSearch integration test FAILED!")
        print(f"   Error: {str(e)}")
        return False


if __name__ == "__main__":
    print("\n🚀 OpenRouter Integration Test Suite")
    print("="*70)
    
    results = []
    
    # Test 1: Basic OpenRouter connection
    results.append(("Basic Connection", test_openrouter_basic()))
    
    # Test 2: Wellness use case
    results.append(("Wellness Use Case", test_openrouter_wellness_use_case()))
    
    # Test 3: OpenDeepSearch integration
    results.append(("OpenDeepSearch Integration", test_opendeepsearch_integration()))
    
    # Summary
    print("\n\n📊 Test Summary")
    print("="*70)
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    total_passed = sum(1 for _, passed in results if passed)
    print(f"\n{total_passed}/{len(results)} tests passed")
    
    if total_passed == len(results):
        print("\n🎉 All tests passed! OpenRouter is ready to use.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
