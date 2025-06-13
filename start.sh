#!/bin/bash

# Set default port if not provided
export PORT=${PORT:-5000}

# Start virtual display for Chrome
echo "Starting Xvfb virtual display..."
Xvfb :99 -screen 0 1280x1024x24 -nolisten tcp -nolisten unix &
export DISPLAY=:99

# Wait for virtual display to start
sleep 3

# Run startup verification
echo "Running startup verification..."
python railway_startup_check.py

# Log startup info
echo ""
echo "=== Starting Railway App ==="
echo "Port: $PORT"
echo "Chrome binary: $(which google-chrome || echo 'NOT FOUND')"
echo "ChromeDriver: $(which chromedriver || echo 'NOT FOUND')"
echo "Display: $DISPLAY"
echo "=========================="
echo ""

# Start the Flask app with gunicorn
exec gunicorn --bind 0.0.0.0:${PORT} \
    --workers 1 \
    --timeout 300 \
    --preload \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    railway_app:app