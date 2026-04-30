# 🧘 Wellness Oracle

**Your AI-Powered Personalized Health Coach**

Wellness Oracle is a web app that analyzes your daily sleep, mood, and activity data to give you personalized health insights. It uses AI (via OpenRouter/DeepSeek) to provide sentiment analysis, burnout risk prediction, and even answers your health questions in real-time. 

## ✨ What it does

- **Daily Logging**: Log your mood and sleep each day.
- **AI Oracle Chat**: Ask health, sleep, or stress-related questions and get intelligent, context-aware answers from the AI.
- **Burnout Prediction**: The system analyzes your history to predict burnout risk and offers interventions.
- **Wearable & Music Integrations**: Connects to **Fitbit** for activity data and **Spotify** to generate personalized mood-boosting playlists (falls back to mock data if you don't connect them).
- **Serverless Database**: Powered by **Firebase Firestore** for fast, reliable data storage.

## 🏗️ Tech Stack
- **Backend:** Python / Flask
- **Database:** Firebase Firestore
- **AI:** OpenRouter (DeepSeek model)
- **Integrations:** Fitbit API, Spotify API (Spotipy)

## 🚀 How to run it locally

1. **Clone & install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Set up Firebase:**
   - Go to the [Firebase Console](https://console.firebase.google.com) and create a Firestore Database (Test mode is fine for local dev).
   - Generate a Service Account JSON key from Project Settings > Service Accounts.
   - Save the file as `serviceAccountKey.json` in the project root.

3. **Set up your Environment:**
   ```bash
   cp .env.template .env
   ```
   Open `.env` and fill in your keys. At minimum, you need an **OpenRouter API Key** and your **Firebase Credentials Path** (`serviceAccountKey.json`).

4. **Start the app:**
   ```bash
   python app.py
   ```
   Visit `http://localhost:5000` in your browser!

## ☁️ Deployment (Render)

If you are deploying to a service like Render:
1. Don't commit `serviceAccountKey.json` to GitHub!
2. In the Render dashboard, go to your Web Service > Environment.
3. You can either:
   - Add a **Secret File** named `serviceAccountKey.json` and set `FIREBASE_CREDENTIALS_PATH=/etc/secrets/serviceAccountKey.json`.
   - **OR** Add an environment variable named `FIREBASE_CREDENTIALS_JSON` and paste the raw JSON contents as the value.

---
*Built to help you build better daily habits through AI.*
