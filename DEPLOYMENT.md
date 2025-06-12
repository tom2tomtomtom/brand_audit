# Brand Audit Tool - Deployment Guide

This guide covers multiple deployment options for the Brand Competitor Analysis Tool.

## Quick Start (Local Development)

### Option 1: Python Virtual Environment (Recommended for Development)

```bash
# 1. Clone/download the project
cd brand-audit-tool

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
cp env_example.txt .env
# Edit .env file and add your OpenAI API key (optional)

# 5. Run the application
python run.py
# Visit http://localhost:5000
```

### Option 2: Direct Flask Run

```bash
# After setting up virtual environment and dependencies
source venv/bin/activate
python app.py
```

## Production Deployment

### Option 1: Docker (Recommended for Production)

```bash
# 1. Ensure Docker and Docker Compose are installed
docker --version
docker-compose --version

# 2. Deploy with the provided script
./deploy.sh

# 3. Application will be available at http://localhost:8000
```

### Option 2: Manual Docker Setup

```bash
# Build the image
docker build -t brand-audit-tool .

# Run the container
docker run -d \
  --name brand-audit-tool \
  -p 8000:8000 \
  -v $(pwd)/results:/app/results \
  -e OPENAI_API_KEY="your_api_key_here" \
  brand-audit-tool
```

### Option 3: Production Server with Gunicorn

```bash
# Install production requirements
pip install -r requirements-prod.txt

# Run with Gunicorn
gunicorn --config gunicorn.conf.py app:app
```

## Cloud Deployment

### AWS EC2 / DigitalOcean / Linode

1. **Launch Ubuntu 20.04+ instance**
2. **Install Docker:**
   ```bash
   sudo apt update
   sudo apt install docker.io docker-compose
   sudo usermod -aG docker $USER
   ```
3. **Deploy the application:**
   ```bash
   git clone <your-repo>
   cd brand-audit-tool
   sudo ./deploy.sh
   ```
4. **Configure firewall:**
   ```bash
   sudo ufw allow 8000
   ```

### Google Cloud Platform

1. **Use Cloud Run for serverless deployment:**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT-ID/brand-audit-tool
   gcloud run deploy --image gcr.io/PROJECT-ID/brand-audit-tool --platform managed
   ```

### Azure Container Instances

1. **Build and push to Azure Container Registry:**
   ```bash
   az acr build --registry myregistry --image brand-audit-tool .
   ```

## Environment Configuration

### Required Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (optional, enables AI analysis)
- `FLASK_ENV`: Set to `production` for production deployment
- `FLASK_DEBUG`: Set to `False` for production

### Optional Configuration

- `MAX_ANALYSIS_TIME`: Maximum analysis time in seconds (default: 600)
- `MAX_CONCURRENT_JOBS`: Maximum concurrent jobs (default: 5)

## Performance Considerations

### Resource Requirements

- **Minimum**: 2GB RAM, 1 CPU core, 10GB storage
- **Recommended**: 4GB RAM, 2 CPU cores, 20GB storage
- **Heavy Usage**: 8GB RAM, 4 CPU cores, 50GB storage

### Scaling

For high-traffic scenarios:
1. Use a load balancer (nginx, HAProxy)
2. Deploy multiple instances
3. Use Redis for job queue management
4. Consider container orchestration (Kubernetes)

## Security Best Practices

### Production Security

1. **Use HTTPS** with SSL certificates
2. **Set up firewall** rules
3. **Regular updates** of dependencies
4. **Monitor logs** for suspicious activity
5. **Backup results** directory regularly

### Docker Security

```bash
# Run as non-root user (already configured in Dockerfile)
# Limit container resources
docker run --memory="2g" --cpus="1.0" brand-audit-tool
```

## Monitoring and Logging

### Application Logs

```bash
# Docker logs
docker-compose logs -f

# Direct logs (when running with Python)
tail -f app.log
```

### Health Checks

The application includes health check endpoints:
- `GET /` - Application status
- Docker health checks are configured automatically

## Troubleshooting

### Common Issues

1. **Chrome/Selenium Issues:**
   ```bash
   # Install Chrome dependencies
   sudo apt-get install -y google-chrome-stable
   ```

2. **Memory Issues:**
   ```bash
   # Increase Docker memory limit
   docker run --memory="4g" brand-audit-tool
   ```

3. **Port Conflicts:**
   ```bash
   # Use different port
   docker run -p 8080:8000 brand-audit-tool
   ```

### Debug Mode

Enable debug logging:
```bash
export FLASK_DEBUG=True
export FLASK_ENV=development
python app.py
```

## Backup and Recovery

### Backup Strategy

1. **Results directory**: Contains generated PDF reports
2. **Configuration files**: `.env`, `gunicorn.conf.py`
3. **Application logs**: For debugging and monitoring

```bash
# Create backup
tar -czf backup-$(date +%Y%m%d).tar.gz results/ .env *.log
```

## Updates and Maintenance

### Updating the Application

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose build
docker-compose restart
```

### Dependency Updates

```bash
# Update Python packages
pip install --upgrade -r requirements.txt

# Rebuild Docker image
docker-compose build --no-cache
```

## Support

For technical issues:
1. Check application logs
2. Verify environment configuration
3. Ensure all dependencies are installed
4. Test with sample data first

The application is designed to be robust and includes comprehensive error handling and fallback mechanisms.