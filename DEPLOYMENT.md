# Netlify Deployment Guide

## Quick Deploy

1. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/yourusername/brand-audit-tool.git
   git push -u origin main
   ```

2. **Deploy on Netlify**:
   - Go to [netlify.com](https://netlify.com)
   - Click "New site from Git"
   - Connect your GitHub repository
   - Netlify will auto-detect the build settings from `netlify.toml`

## Build Settings (Auto-configured)

- **Build command**: `npm run build`
- **Publish directory**: `.next`
- **Node version**: 18
- **Functions directory**: Auto-detected

## Environment Variables (Optional)

In Netlify dashboard > Site settings > Environment variables:

```
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

**Note**: The tool works fully without API keys using intelligent fallbacks!

## Features Ready for Testing

✅ **Universal Brand Analysis** - Works with any industry
✅ **Visual Asset Extraction** - Logos, colors, fonts
✅ **Comprehensive Reports** - SWOT, positioning, digital scores
✅ **Multi-format Exports** - PDF, HTML, JSON downloads
✅ **Medical Industry Examples** - Test with Wolters Kluwer, Elsevier, Open Evidence

## Post-Deployment Testing

Test these endpoints after deployment:
- `/` - Main application interface
- `/api/analyze` - Brand analysis API
- `/api/download/html` - HTML report export
- `/api/download/json` - JSON data export

## Troubleshooting

- If builds fail, check Node version is set to 18
- API routes work as Netlify Functions automatically
- All dependencies are properly configured for serverless deployment