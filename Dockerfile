FROM python:3.11

WORKDIR /app

# Fixed ChromeDriver installation - Dec 13, 2024

# Install system dependencies including Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libdrm2 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    libgbm1 \
    ca-certificates \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/googlechrome-linux-keyring.gpg \
    && sh -c 'echo "deb [arch=amd64 signed-by=/usr/share/keyrings/googlechrome-linux-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/* \
    && google-chrome --version

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install ChromeDriver using webdriver-manager (handles version compatibility automatically)
RUN echo "Installing ChromeDriver via webdriver-manager..." && \
    python -c "
from webdriver_manager.chrome import ChromeDriverManager
import shutil
import os
print('Downloading compatible ChromeDriver...')
driver_path = ChromeDriverManager().install()
print(f'Downloaded to: {driver_path}')
shutil.copy(driver_path, '/usr/local/bin/chromedriver')
os.chmod('/usr/local/bin/chromedriver', 0o755)
print('ChromeDriver installed successfully')
" && \
    echo "Verifying ChromeDriver installation..." && \
    chromedriver --version && \
    echo "ChromeDriver setup complete!"

# Copy application files
COPY strategic_competitive_intelligence.py .
COPY railway_app.py .
COPY railway_startup_check.py .
COPY railway_health_only.py .
COPY deep_scraper.py .

# Create required directories
RUN mkdir -p /tmp

# Set environment variables for Chrome
ENV DISPLAY=:99
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROMEDRIVER_PATH=/usr/local/bin/chromedriver

# Health check with longer timeout for Railway
HEALTHCHECK --interval=60s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:${PORT:-5000}/health || exit 1

# Expose port
EXPOSE $PORT

# Create startup script
COPY start.sh .
RUN chmod +x start.sh

# Run the app with gunicorn for production
CMD ["./start.sh"]