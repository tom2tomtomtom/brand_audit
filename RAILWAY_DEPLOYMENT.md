# Railway Deployment Guide

Railway is the recommended platform for deploying this Flask application with full functionality.

## 🚀 Quick Railway Deployment

### Method 1: Railway CLI (Recommended)

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login to Railway
railway login

# 3. Initialize project (in your project directory)
railway init

# 4. Deploy
railway up
```

### Method 2: GitHub Integration (Easy)

1. Go to [railway.app](https://railway.app)
2. Sign up/login with GitHub
3. Click "New Project"
4. Choose "Deploy from GitHub repo"
5. Select: `tom2tomtomtom/brand_audit`
6. Railway will automatically detect it's a Python app and deploy

## ⚙️ Configuration

### Environment Variables (Optional but Recommended)

After deployment, add environment variables in Railway dashboard:

1. Go to your project dashboard
2. Click "Variables" tab
3. Add these variables:

```bash
OPENAI_API_KEY=your_actual_openai_api_key_here
FLASK_ENV=production
FLASK_DEBUG=False
MAX_ANALYSIS_TIME=600
MAX_CONCURRENT_JOBS=3
```

### Domain Configuration

Railway provides a default domain like: `your-app-name.up.railway.app`

To use a custom domain:
1. Go to "Settings" tab
2. Add your custom domain
3. Configure DNS records as shown

## 🔧 Railway Configuration Files

The repository includes Railway-optimized files:

- `railway.json` - Railway deployment configuration
- `nixpacks.toml` - Build configuration with Chrome/Chromium
- `gunicorn.conf.py` - Production server configuration
- `requirements.txt` - Python dependencies

## ✅ What Works on Railway

✅ **Full Functionality Available:**
- Long-running analysis processes (5-10 minutes)
- Selenium WebDriver with Chrome/Chromium
- OpenAI API integration
- PDF report generation
- Background job processing
- File system access for results storage

✅ **Railway Advantages:**
- Automatic HTTPS
- Zero-config deployments
- Git-based deployments
- Reasonable pricing
- Excellent Python support
- Built-in monitoring

## 🧪 Testing Your Deployment

1. **Access your app:** Visit your Railway URL
2. **Check platform detection:** Should show "✅ Railway Deployment Detected"
3. **Test analysis:** Try with sample URLs:
   - https://stripe.com
   - https://github.com
   - https://shopify.com

## 🐛 Troubleshooting

### Common Issues:

**Build Fails:**
```bash
# Check build logs in Railway dashboard
# Usually related to missing dependencies
```

**Chrome/Selenium Issues:**
```bash
# Ensure nixpacks.toml includes chromium and chromedriver
# This is already configured in the repository
```

**Memory Issues:**
```bash
# Upgrade Railway plan if needed
# Default plan should handle 3-5 brand analysis
```

**Environment Variables:**
```bash
# Add OPENAI_API_KEY in Railway dashboard
# App works without it but with limited analysis capability
```

## 💰 Pricing

- **Hobby Plan:** $5/month - Perfect for this application
- **Pro Plan:** $20/month - For heavy usage
- **Free Trial:** Available for testing

## 📊 Expected Performance

- **Deployment Time:** 2-3 minutes
- **Analysis Time:** 5-10 minutes per job
- **Concurrent Users:** 5-10 (depending on plan)
- **Uptime:** 99.9%

## 🎯 Post-Deployment Steps

1. **Test functionality** with sample brand URLs
2. **Add OpenAI API key** for enhanced analysis
3. **Configure custom domain** (optional)
4. **Set up monitoring/alerts** in Railway dashboard
5. **Share your deployed app** with stakeholders

## 🔗 Useful Links

- [Railway Documentation](https://docs.railway.app/)
- [Railway CLI](https://docs.railway.app/develop/cli)
- [Python on Railway](https://docs.railway.app/guides/python)

Your app will be available at: `https://your-project-name.up.railway.app`