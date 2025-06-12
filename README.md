# Brand Competitor Analysis Tool

A comprehensive Flask-based web application that performs automated brand analysis and generates professional PDF reports comparing multiple competitors.

## Features

- **Comprehensive Web Scraping**: Deep analysis of competitor websites using Selenium and BeautifulSoup
- **AI-Powered Analysis**: Uses OpenAI GPT-4 for intelligent brand positioning and strategy insights
- **Professional PDF Reports**: Generates detailed competitive analysis reports with charts and recommendations
- **Real-Time Progress Tracking**: Live updates during the 5-10 minute analysis process
- **Visual Asset Extraction**: Automatically extracts logos, colors, fonts, and brand elements
- **Multi-Page Analysis**: Analyzes homepages, about pages, product pages, news sections, and more

## Analysis Output

The tool generates comprehensive reports including:

- **Executive Summary**: High-level competitive landscape overview
- **Individual Brand Profiles**: Detailed analysis of each competitor
- **Brand Identity Assessment**: Logo, colors, fonts, personality, positioning
- **Digital Presence Scores**: Website quality, UX, content, SEO ratings
- **Competitive Analysis**: Strengths, weaknesses, opportunities, threats
- **Strategic Recommendations**: Immediate, medium-term, and long-term action items
- **Comparative Benchmarking**: Performance comparison across all analyzed brands

## Installation

### Prerequisites

- Python 3.8 or higher
- Chrome browser (for Selenium WebDriver)
- OpenAI API key (optional, for enhanced AI analysis)

### Setup Instructions

1. **Clone or download the project files**

2. **Create a Python virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp env_example.txt .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_openai_api_key_here
   ```

5. **Create required directories**:
   ```bash
   mkdir -p results static templates
   ```

## Usage

### Start the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Perform Analysis

1. Open your browser and navigate to `http://localhost:5000`
2. Enter 3-5 competitor brand URLs (minimum 3 required)
3. Click "Start Brand Analysis"
4. Monitor real-time progress (5-10 minutes total)
5. Download the generated PDF report when complete

### Sample URLs for Testing

You can test the tool with these sample URLs:
- https://wolterskluwer.com
- https://medscape.com  
- https://uptodate.com
- https://stripe.com
- https://shopify.com

## Technical Architecture

### Backend Components

- **Flask Web Framework**: RESTful API endpoints and web server
- **Selenium WebDriver**: Browser automation for JavaScript-heavy sites
- **BeautifulSoup**: HTML parsing and content extraction
- **OpenAI GPT-4**: AI-powered brand analysis and insights
- **ReportLab**: Professional PDF report generation
- **Threading**: Asynchronous analysis processing

### Frontend Components

- **HTML5/CSS3**: Modern responsive web interface
- **Tailwind CSS**: Utility-first styling framework
- **Vanilla JavaScript**: Real-time progress tracking and API communication
- **Progressive Enhancement**: Works without JavaScript for basic functionality

### Analysis Pipeline

1. **Input Validation**: Verify URLs and format requirements
2. **Web Scraping**: 
   - Load pages with Selenium browser automation
   - Extract content with BeautifulSoup parsing
   - Analyze multiple page types (home, about, products, news)
   - Extract visual assets (logos, colors, fonts)
3. **Content Analysis**:
   - Industry detection and categorization
   - Brand personality and positioning assessment
   - Technical infrastructure evaluation
4. **AI Processing**:
   - GPT-4 brand strategy analysis
   - Competitive positioning insights
   - Strategic recommendations generation
5. **Report Generation**:
   - Professional PDF layout with charts
   - Executive summary and detailed findings
   - Comparative analysis and benchmarking

## API Endpoints

- `GET /` - Main application interface
- `POST /api/analyze` - Start new analysis job
- `GET /api/progress/<job_id>` - Get analysis progress
- `GET /api/result/<job_id>` - Download completed PDF report

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key for enhanced AI analysis
- `FLASK_ENV`: Set to 'development' for debugging
- `FLASK_DEBUG`: Enable/disable debug mode
- `MAX_ANALYSIS_TIME`: Maximum analysis time in seconds (default: 600)
- `MAX_CONCURRENT_JOBS`: Maximum concurrent analysis jobs (default: 5)

### Analysis Timing

- **Total Time**: 5-10 minutes for 3-5 brands
- **Per Brand**: 1-2 minutes scraping + 30-60 seconds AI analysis
- **Report Generation**: 30-60 seconds

## Output Examples

### PDF Report Structure

1. **Cover Page**: Professional branding with analysis details
2. **Executive Summary**: Key findings and market overview
3. **Individual Brand Analysis**: Detailed profiles for each competitor
4. **Comparative Analysis**: Side-by-side performance comparison
5. **Strategic Recommendations**: Actionable insights and next steps

### Analysis Metrics

- Overall competitive score (0-100)
- Digital presence assessment (website, UX, content, SEO)
- Brand identity evaluation (personality, positioning, messaging)
- Technical implementation review (performance, security, standards)

## Troubleshooting

### Common Issues

1. **Chrome Driver Issues**: 
   - Ensure Chrome browser is installed
   - WebDriver Manager automatically handles driver installation

2. **OpenAI API Errors**:
   - Verify API key is correct and has sufficient credits
   - Tool falls back to rule-based analysis if API unavailable

3. **Website Access Issues**:
   - Some sites may block automated scraping
   - Tool includes fallback data generation for inaccessible sites

4. **Memory Issues**:
   - Large websites may require more RAM
   - Consider reducing concurrent job limit

### Performance Optimization

- **Concurrent Analysis**: Tool processes brands in parallel where possible
- **Caching**: Implements intelligent caching for repeated requests
- **Resource Management**: Automatically cleans up browser sessions and temporary files

## Security Considerations

- **Data Privacy**: No persistent storage of analyzed data
- **Rate Limiting**: Respectful delays between requests to avoid overloading target sites
- **Input Validation**: Comprehensive URL and parameter validation
- **Safe Browsing**: Sandboxed browser execution with security restrictions

## Development

### Project Structure

```
brand-audit-tool/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── env_example.txt       # Environment variables template
├── src/                  # Source code modules
│   ├── __init__.py
│   ├── scraper.py        # Web scraping functionality
│   ├── analyzer.py       # AI analysis and insights
│   ├── report_generator.py  # PDF report creation
│   └── progress_tracker.py  # Job progress management
├── templates/            # HTML templates
│   └── index.html        # Main web interface
├── static/              # Static assets (CSS, JS, images)
├── results/             # Generated PDF reports (auto-created)
└── .env                 # Environment variables (create from example)
```

### Extending the Tool

- **Additional Analysis**: Extend `analyzer.py` with new metrics
- **Custom Reports**: Modify `report_generator.py` for different layouts
- **New Data Sources**: Add social media, SEO tools, or other APIs
- **Enhanced UI**: Improve frontend with React/Vue.js framework

## License

This project is for educational and internal business use. Ensure compliance with target websites' robots.txt and terms of service when performing analysis.

## Support

For technical issues or feature requests, please review the code comments and error logs for troubleshooting guidance.