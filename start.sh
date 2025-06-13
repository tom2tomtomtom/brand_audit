#!/bin/bash

# Set default port if not provided
export PORT=${PORT:-5000}

# Start virtual display for Chrome (in background, don't wait)
echo "Starting Xvfb virtual display..."
Xvfb :99 -screen 0 1280x1024x24 -nolisten tcp -nolisten unix &
export DISPLAY=:99

# Log startup info
echo ""
echo "=== Starting Brandintell App ==="
echo "Port: $PORT"
echo "Display: $DISPLAY"
echo "=========================="
echo ""

# Start the Flask app with gunicorn (increased timeout for startup)
exec gunicorn --bind 0.0.0.0:${PORT} \
    --workers 1 \
    --threads 4 \
    --timeout 300 \
    --graceful-timeout 60 \
    --preload \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    railway_app_async:app