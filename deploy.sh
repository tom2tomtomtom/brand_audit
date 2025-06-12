#!/bin/bash

# Brand Audit Tool Deployment Script

set -e

echo "🚀 Starting Brand Audit Tool Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

print_status "Docker and Docker Compose found"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    print_warning "Creating .env file from template..."
    cp env_example.txt .env
    print_warning "Please edit .env file and add your OpenAI API key if desired"
fi

# Create results directory
mkdir -p results
mkdir -p static
mkdir -p templates

print_status "Directories created"

# Build and start the application
echo "🏗️  Building Docker image..."
docker-compose build

echo "🚀 Starting application..."
docker-compose up -d

# Wait for the application to start
echo "⏳ Waiting for application to start..."
sleep 10

# Check if the application is running
if curl -f http://localhost:8000/ > /dev/null 2>&1; then
    print_status "Application is running successfully!"
    echo ""
    echo "🌐 Application URL: http://localhost:8000"
    echo "📊 You can now perform brand analysis!"
    echo ""
    echo "To stop the application, run: docker-compose down"
    echo "To view logs, run: docker-compose logs -f"
    echo "To restart, run: docker-compose restart"
else
    print_error "Application failed to start properly"
    echo "Check logs with: docker-compose logs"
    exit 1
fi