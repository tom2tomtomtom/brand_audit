# Netlify Deployment Setup

## Required Environment Variables

Set these environment variables in your Netlify dashboard under Site Settings > Environment Variables:

### Supabase Configuration
```
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
```

### AI APIs (Optional - for analysis features)
```
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```

### Other Configuration
```
NEXTAUTH_SECRET=your_nextauth_secret_here
NEXTAUTH_URL=https://your-site.netlify.app
NODE_ENV=production
```

## Deployment Steps

1. **Set Environment Variables**: Add all required environment variables in Netlify dashboard
2. **Connect Repository**: Connect your GitHub repository to Netlify
3. **Configure Build Settings**:
   - Build command: `npm run build`
   - Publish directory: `.next`
4. **Deploy**: Trigger a new deployment

## Troubleshooting

If you get "supabaseUrl is required" error:
- Check that `NEXT_PUBLIC_SUPABASE_URL` is set in Netlify environment variables
- Ensure the URL starts with `https://` and ends with `.supabase.co`
- Verify the anon key is correctly copied from Supabase dashboard

If you get "Missing service role key" error:
- Check that `SUPABASE_SERVICE_ROLE_KEY` is set
- This key should be the service_role key from Supabase (not the anon key)