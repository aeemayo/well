#!/bin/bash

# OpenRouter Integration Setup Script
# Automates the setup process for OpenRouter + Open Deep Search integration

echo "=========================================="
echo "🚀 OpenRouter Integration Setup"
echo "=========================================="
echo ""

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Warning: No virtual environment detected"
    echo "   Consider activating one first:"
    echo "   source well_env/bin/activate"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    if [ -f .env.template ]; then
        cp .env.template .env
        echo "✅ .env file created from template"
    else
        echo "❌ .env.template not found!"
        exit 1
    fi
else
    echo "✅ .env file already exists"
fi

# Check for OPENROUTER_API_KEY
if ! grep -q "OPENROUTER_API_KEY" .env; then
    echo ""
    echo "⚠️  OPENROUTER_API_KEY not found in .env"
    echo ""
    read -p "Do you have an OpenRouter API key? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter your OpenRouter API key: " api_key
        echo "OPENROUTER_API_KEY=$api_key" >> .env
        echo "✅ API key added to .env"
    else
        echo ""
        echo "ℹ️  Get your API key from: https://openrouter.ai/"
        echo "   Then add it to .env file:"
        echo "   OPENROUTER_API_KEY=sk-your-key-here"
        echo ""
    fi
fi

# Check if openai package is installed
echo ""
echo "📦 Checking dependencies..."
python -c "import openai" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ openai package is installed"
else
    echo "⚠️  openai package not found"
    read -p "Install now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pip install openai
    fi
fi

# Check if opendeepsearch is installed
python -c "import opendeepsearch" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ opendeepsearch package is installed"
else
    echo "⚠️  opendeepsearch package not found"
    read -p "Install from requirements.txt? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pip install git+https://github.com/sentient-agi/OpenDeepSearch.git
    fi
fi

# Check if dspy is installed
python -c "import dspy" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ dspy package is installed"
else
    echo "⚠️  dspy package not found"
    read -p "Install now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pip install dspy-ai
    fi
fi

# Run tests
echo ""
echo "=========================================="
echo "🧪 Running Integration Tests"
echo "=========================================="
echo ""

if [ -f test_openrouter.py ]; then
    python test_openrouter.py
    test_result=$?
    
    if [ $test_result -eq 0 ]; then
        echo ""
        echo "=========================================="
        echo "✅ Setup Complete!"
        echo "=========================================="
        echo ""
        echo "Next steps:"
        echo "1. Review your .env file"
        echo "2. Try examples: python examples_openrouter.py"
        echo "3. Start app: python app.py"
        echo ""
        echo "OpenRouter Documentation: https://openrouter.ai/docs"
        echo ""
    else
        echo ""
        echo "=========================================="
        echo "⚠️  Tests Failed"
        echo "=========================================="
        echo ""
        echo "Please check:"
        echo "1. OPENROUTER_API_KEY is valid"
        echo "2. API key has credits"
        echo "3. Internet connection is working"
        echo ""
        echo "See https://openrouter.ai/docs for troubleshooting"
        echo ""
    fi
else
    echo "⚠️  test_openrouter.py not found"
    echo "   Skipping tests"
fi
