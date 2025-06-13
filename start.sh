#!/bin/bash

# Start the Flask app with gunicorn
exec gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 1 --timeout 300 --preload railway_app:app