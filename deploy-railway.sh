#!/bin/bash

# Railway Deployment Script for Brand Audit Tool

echo "🚂 Starting Railway deployment..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

# Check if logged in
echo "🔐 Checking Railway login status..."
if ! railway status &> /dev/null; then
    echo "🔑 Please login to Railway:"
    railway login
fi

# Initialize project if needed
if [ ! -f "railway.toml" ]; then
    echo "🎯 Initializing Railway project..."
    railway init
fi

# Deploy the application
echo "🚀 Deploying to Railway..."
railway up

# Get the deployment URL
echo "🌐 Getting deployment URL..."
RAILWAY_URL=$(railway status --json | grep -o '"url":"[^"]*' | cut -d'"' -f4)

if [ -n "$RAILWAY_URL" ]; then
    echo "✅ Deployment successful!"
    echo "🔗 Your app is available at: $RAILWAY_URL"
    echo ""
    echo "📋 Next steps:"
    echo "1. Visit your app: $RAILWAY_URL"
    echo "2. Add OpenAI API key in Railway dashboard for full functionality"
    echo "3. Test with sample brand URLs"
    echo ""
    echo "💡 To add environment variables:"
    echo "   railway variables set OPENAI_API_KEY=your_api_key_here"
else
    echo "⚠️  Deployment completed but couldn't get URL"
    echo "   Check Railway dashboard for your app URL"
fi

echo "🎉 Railway deployment complete!"