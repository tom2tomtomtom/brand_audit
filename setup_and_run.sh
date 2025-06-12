#!/bin/bash

# Exit on error
set -e

echo "===== Setting up the Competitor Intelligence Platform ====="

# Check if a virtual environment exists, create it if it doesn't
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install backend dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install frontend dependencies
echo "Setting up the React frontend..."
cd frontend
npm install
cd ..

# Prompt for OpenAI API key if not set
if [ -z "$OPENAI_API_KEY" ] && [ ! -f ".env" ]; then
  echo "OpenAI API Key not found."
  read -p "Enter your OpenAI API key: " api_key
  echo "OPENAI_API_KEY=$api_key" > .env
  echo "API key saved to .env file."
fi

# Start backend (in background)
echo "Starting Flask backend server..."
nohup python app.py > flask_server.log 2>&1 &
FLASK_PID=$!
echo "Flask server started with PID: $FLASK_PID"

# Wait for Flask to start up
echo "Waiting for Flask server to start..."
sleep 5

# Start frontend
echo "Starting React development server..."
cd frontend
npm start

# When the React process exits, kill the Flask server
echo "Stopping Flask server..."
kill $FLASK_PID
echo "All services stopped."