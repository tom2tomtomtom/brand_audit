# 🚀 Brand Audit Tool - Deployment Guide

## 📋 Prerequisites

- GitHub account
- Supabase account
- OpenAI API account
- Netlify account (for deployment)

## 🔧 Setup Instructions

### 1. **Clone the Repository**
```bash
git clone https://github.com/tom2tomtomtom/brand_audit.git
cd brand_audit
npm install
```

### 2. **Supabase Setup**

1. **Create a new Supabase project**
   - Go to [supabase.com](https://supabase.com)
   - Create a new project
   - Note your project URL and anon key

2. **Run the database setup**
   - Open the Supabase SQL editor
   - Copy and paste the contents of `database_setup.sql`
   - Execute the script

3. **Configure storage buckets**
   - Go to Storage in Supabase dashboard
   - Create buckets: `assets`, `presentations`
   - Set appropriate permissions

### 3. **Environment Variables**

Copy `.env.example` to `.env.local` and fill in your values:

```env
# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

# AI APIs
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# App Configuration
NEXT_PUBLIC_APP_URL=https://your-domain.netlify.app
NODE_ENV=production
```

### 4. **Local Development**

```bash
npm run dev
```

Visit `http://localhost:3000` to test the application.

### 5. **Netlify Deployment**

1. **Connect to Netlify**
   - Go to [netlify.com](https://netlify.com)
   - Connect your GitHub repository
   - Choose the `brand_audit` repository

2. **Configure Build Settings**
   - Build command: `npm run build`
   - Publish directory: `.next`
   - Node version: 18

3. **Environment Variables**
   - Add all environment variables from your `.env.local`
   - Make sure to use production URLs

4. **Deploy**
   - Netlify will automatically deploy on every push to main
   - Check the deployment logs for any issues

## 🔐 Security Checklist

- [ ] Environment variables are set correctly
- [ ] Supabase RLS policies are enabled
- [ ] API keys are kept secure
- [ ] Database backups are configured
- [ ] SSL/HTTPS is enabled

## 📊 Monitoring

### **Health Check**
- Visit `/api/health` to check API status
- Monitor Supabase dashboard for database health
- Check Netlify deployment logs

### **Usage Monitoring**
- Admin users can access `/api/admin/stats`
- Monitor API usage in OpenAI dashboard
- Track costs and rate limits

## 🐛 Troubleshooting

### **Common Issues**

1. **Database Connection Errors**
   - Check Supabase URL and keys
   - Verify RLS policies are set up
   - Ensure database functions exist

2. **API Rate Limits**
   - Check OpenAI API usage
   - Verify rate limiting configuration
   - Monitor cost tracking

3. **Build Failures**
   - Check Node.js version (18+)
   - Verify all dependencies are installed
   - Check TypeScript compilation

### **Debug Steps**

1. Check browser console for errors
2. Review Netlify deployment logs
3. Check Supabase logs
4. Verify environment variables

## 📈 Scaling Considerations

### **Performance Optimization**
- Enable Supabase connection pooling
- Configure CDN for static assets
- Implement caching strategies
- Monitor database performance

### **Cost Management**
- Set up OpenAI usage alerts
- Monitor Supabase usage
- Implement user quotas
- Track monthly costs

## 🔄 Updates and Maintenance

### **Regular Tasks**
- Monitor API usage and costs
- Update dependencies
- Review security policies
- Backup database regularly

### **Feature Updates**
- Test in development first
- Use feature flags for gradual rollout
- Monitor deployment health
- Have rollback plan ready

## 📞 Support

For deployment issues:
1. Check the troubleshooting section
2. Review GitHub issues
3. Check Supabase documentation
4. Contact support if needed

---

**Your Brand Audit Tool is now ready for production! 🎉**
