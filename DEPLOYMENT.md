# Deployment Guide - Render

## Important: Database Configuration

### ⚠️ SQLite Limitation on Render
**SQLite databases on Render are EPHEMERAL** - they are reset on every deployment. This means all user data will be lost when you redeploy.

### Recommended Solution: Use PostgreSQL

For production on Render, you should use PostgreSQL instead of SQLite:

#### 1. Create a PostgreSQL Database on Render
1. Go to your Render dashboard
2. Click "New" → "PostgreSQL"
3. Choose a name (e.g., "wellness-db")
4. Select the free tier
5. Click "Create Database"

#### 2. Get the Internal Database URL
After creation, copy the **Internal Database URL** from the database info page.

#### 3. Set Environment Variable
In your Render web service:
1. Go to "Environment" tab
2. Add a new environment variable:
   - **Key:** `DATABASE_URL`
   - **Value:** Paste the Internal Database URL

#### 4. Update Your Config (Already Done!)
The app will automatically detect and use `DATABASE_URL` if it's set.

#### 5. Add psycopg2 to requirements.txt
You need the PostgreSQL adapter:
```bash
psycopg2-binary>=2.9.9
```

### Current Fix Applied

The app has been updated to:
1. **Automatically create database tables on startup** - This fixes the "no such table: users" error
2. **Support both SQLite (dev) and PostgreSQL (production)** via environment variables
3. **Create necessary folders** (uploads, instance) on startup

### Testing the Fix

After pushing these changes to Render:
1. The database tables will be created automatically
2. The login page should work (though users won't persist with SQLite)
3. Check logs to confirm: "Database initialized successfully"

### For Persistent Storage (Recommended)

Follow the PostgreSQL setup above to ensure:
- ✅ User data persists across deployments
- ✅ Better performance for production
- ✅ Scalability for multiple users
- ✅ Transaction safety

## Environment Variables on Render

Make sure these are set in your Render web service:

### Required:
- `SECRET_KEY` - A strong random secret key
- `OPENROUTER_API_KEY` - Your OpenRouter API key

### Recommended:
- `DATABASE_URL` - PostgreSQL connection string (see above)

### Optional (for integrations):
- `FITBIT_CLIENT_ID`
- `FITBIT_CLIENT_SECRET`
- `FITBIT_REDIRECT_URI` - Update to your Render URL
- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`
- `SPOTIFY_REDIRECT_URI` - Update to your Render URL

## Deployment Checklist

- [x] Database tables auto-created on startup
- [ ] Set `SECRET_KEY` environment variable
- [ ] Set `OPENROUTER_API_KEY` environment variable
- [ ] Set up PostgreSQL database (recommended)
- [ ] Update OAuth redirect URIs to Render URL
- [ ] Test login functionality
- [ ] Monitor logs for errors

## Troubleshooting

### "no such table" errors
- Fixed! Tables now created automatically on startup
- Check logs for "Database initialized successfully"

### Data disappears after deployment
- Switch to PostgreSQL (see instructions above)
- SQLite is ephemeral on Render

### Login still not working
- Check that SECRET_KEY is set
- Verify database tables were created (check logs)
- Try creating a new user

## Additional Notes

- Gunicorn is used as the production server
- Database initialization happens when `app.py` is imported
- Scheduler for daily nudges starts automatically
- Logs are available in Render dashboard
