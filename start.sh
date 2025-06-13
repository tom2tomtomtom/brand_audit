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

# Start the Flask app with gunicorn (reduced timeout, increased graceful timeout)
exec gunicorn --bind 0.0.0.0:${PORT} \
    --workers 1 \
    --timeout 120 \
    --graceful-timeout 30 \
    --access-logfile - \
    --error-logfile - \
    --log-level debug \
    railway_app:app