#!/bin/bash

# Set default port if not provided
export PORT=${PORT:-5000}

# Start virtual display for Chrome
echo "Starting Xvfb virtual display..."
Xvfb :99 -screen 0 1280x1024x24 -nolisten tcp -nolisten unix &
export DISPLAY=:99

# Wait for virtual display to start
sleep 3

# Pre-install ChromeDriver using webdriver-manager
echo "Pre-installing ChromeDriver..."
python -c "from webdriver_manager.chrome import ChromeDriverManager; print('Installing ChromeDriver...'); ChromeDriverManager().install(); print('ChromeDriver ready')" || echo "ChromeDriver pre-install failed, will retry at runtime"

# Log startup info
echo ""
echo "=== Starting Brandintell App ==="
echo "Port: $PORT"
echo "Chrome binary: $(which google-chrome || echo 'Will use from /usr/bin/google-chrome-stable')"
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