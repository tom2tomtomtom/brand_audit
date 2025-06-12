# Netlify Deployment Guide

## ⚠️ Important Limitations

**Netlify Functions are not suitable for this Flask application** due to several technical constraints:

### Why Netlify Won't Work Properly

1. **15-second timeout**: Analysis takes 5-10 minutes per job
2. **No persistent storage**: Cannot save PDF reports
3. **Limited packages**: Selenium WebDriver not supported
4. **No background processes**: Cannot run long-running scraping tasks
5. **Memory constraints**: Complex AI analysis exceeds limits

## 🚀 Recommended Deployment Options

### Option 1: Docker (Recommended)
```bash
# Local deployment
docker-compose up

# Production deployment
./deploy.sh
```

### Option 2: Heroku
```bash
# Install Heroku CLI
npm install -g heroku

# Create Heroku app
heroku create your-brand-audit-tool

# Add Python buildpack
heroku buildpacks:set heroku/python

# Set environment variables
heroku config:set OPENAI_API_KEY=your_key_here

# Deploy
git push heroku main
```

### Option 3: Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Option 4: DigitalOcean App Platform
1. Connect your GitHub repository
2. Choose Python app
3. Set build command: `pip install -r requirements.txt`
4. Set run command: `gunicorn --config gunicorn.conf.py app:app`
5. Add environment variables

### Option 5: Google Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT-ID/brand-audit-tool
gcloud run deploy --image gcr.io/PROJECT-ID/brand-audit-tool --platform managed
```

## 📝 What's Deployed on Netlify

The Netlify deployment includes:
- Static informational page explaining limitations
- Links to proper deployment options
- Basic error handling for API calls
- Repository information

## 🔧 Files for Netlify

- `netlify.toml` - Build configuration
- `netlify/functions/app.py` - Function handler
- `public/index.html` - Static page
- `requirements-netlify.txt` - Minimal dependencies

## ✅ Testing the Netlify Deployment

1. Push to GitHub
2. Connect repository to Netlify
3. Deploy automatically
4. Visit site to see deployment notice

The site will explain why full functionality isn't available and provide proper deployment instructions.

## 🎯 Conclusion

While we can deploy a static informational site to Netlify, **the Flask application requires a proper server environment** for full functionality. Use Docker, Heroku, Railway, or similar platforms for production deployment.