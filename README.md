# Competitor Intelligence Platform

This project focuses on automating the process of gathering and filtering relevant market insights using Python and OpenAI. It is specifically built for analyzing competitors in the gut health industry, and now features a user-friendly web interface.

## Key Components

1. **News Article Filtering**: Leverages OpenAI's API to analyze news articles and determine their relevance to a specific industry. The filtered results are structured and saved for easy analysis.

2. **Web Scraping for Competitor Insights**: A web scraper designed to extract key product and company details from competitor websites, organizing the data into a structured format.

3. **Interactive UI**: A React.js frontend that guides users through the process of analyzing competitors and generating detailed reports.

## Features

- Analyze your website to identify potential competitors
- Scrape and analyze competitor websites to extract company and product information
- Filter news articles related to gut health products
- Generate comprehensive competitor intelligence reports
- Interactive wizard UI to guide you through the competitor analysis process

## Setup Instructions

### Backend Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```
   - On Windows:
     ```
     venv\Scripts\activate
     ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your OpenAI API key or export it to your environment:
   ```
   # In .env file
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Or in terminal
   export OPENAI_API_KEY="your key here"
   ```

5. Run the Flask server:
   ```
   python app.py
   ```
   The server will run on http://127.0.0.1:8080

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install Node.js dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```
   The React app will run on http://localhost:3000

## API Endpoints

- `/scrape_competitor` (POST): Scrape and analyze a competitor website
- `/filter_news` (GET): Filter news articles about gut health products
- `/download/<filename>` (GET): Download processed data files
- `/api/find-competitors` (POST): Identify potential competitors for a given website
- `/api/generate-report` (POST): Generate a competitor intelligence report

## Project Structure

- `app.py`: Flask backend application
- `Project/`: Directory containing Python scripts for competitor analysis
  - `Competitor and Product Profiler.py`: Scrapes websites for competitor info
  - `Filtering News Articles.py`: Filters news articles about gut health
  - `Website Content Filter.py`: Filters website content
- `frontend/`: React.js frontend application
  - `src/components/`: React components
  - `public/`: Static files

## Technologies Used

- Backend:
  - Flask
  - OpenAI API
  - Pandas
  - Beautiful Soup
  - Python-dotenv

- Frontend:
  - React.js
  - Bootstrap
  - Axios
