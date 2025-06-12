# Gunicorn configuration for production deployment
import os

# Server socket - Railway uses PORT environment variable
port = os.environ.get("PORT", "8000")
bind = f"0.0.0.0:{port}"
backlog = 2048

# Worker processes - Optimized for Railway
workers = int(os.environ.get("WEB_CONCURRENCY", "2"))
worker_class = "sync" 
worker_connections = 1000
timeout = 120  # Increased for longer analysis requests
keepalive = 2
max_requests = 1000
max_requests_jitter = 100

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "brand-audit-tool"

# Server mechanics
daemon = False
pidfile = "/tmp/brand-audit-tool.pid"
tmp_upload_dir = None

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190