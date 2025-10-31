# Git Commit Instructions

## Ready to Deploy!

Use these commands to commit and push your fixes:

```bash
cd /home/aeem/well

# Stage all changes
git add app.py config.py requirements.txt DEPLOYMENT.md FIX_SUMMARY.md

# Commit with a descriptive message
git commit -m "Fix: Auto-initialize database tables on Render startup

- Add automatic database table creation when app starts
- Fix 'no such table: users' error on Render
- Add PostgreSQL support via DATABASE_URL environment variable
- Add psycopg2-binary for PostgreSQL driver
- Create upload folders automatically
- Add comprehensive deployment documentation

This fixes the SQLite initialization issue where tables weren't
being created when Gunicorn imported the app on Render."

# Push to your repository
git push origin clean-main
```

## After Pushing

1. **Render will automatically redeploy** (if you have auto-deploy enabled)
2. **Monitor the logs** to see "Database initialized successfully"
3. **Test the login** - it should work now!

## Optional: Set Up PostgreSQL (Recommended)

For persistent data storage, follow the instructions in `DEPLOYMENT.md`:
- Create a PostgreSQL database on Render (free tier available)
- Add `DATABASE_URL` environment variable to your web service
- Data will persist across deployments

## Environment Variables to Set on Render

Go to your web service → Environment tab:

**Required:**
- `SECRET_KEY` - Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`
- `OPENROUTER_API_KEY` - Your OpenRouter API key

**Recommended (for persistent storage):**
- `DATABASE_URL` - Your PostgreSQL connection string

**Optional (for OAuth features):**
- `FITBIT_CLIENT_ID`
- `FITBIT_CLIENT_SECRET`
- `FITBIT_REDIRECT_URI` - Update to: `https://well-xfjz.onrender.com/fitbit/callback`
- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`
- `SPOTIFY_REDIRECT_URI` - Update to: `https://well-xfjz.onrender.com/spotify/callback`
