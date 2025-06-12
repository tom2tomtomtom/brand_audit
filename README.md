# Brand Competitor Analysis & Grid Generator

A comprehensive brand analysis platform that scrapes competitor websites, analyzes brand elements, and generates professional competitive landscape reports.

## 🚀 Features

### Core Analysis Capabilities
- **Live Data Extraction**: Zero placeholder data - only real extracted information
- **5-Row Competitive Grid**: Exactly as specified with logos, positioning, personality, colors, and visuals
- **AI-Powered Insights**: Uses OpenAI GPT-4 for intelligent brand analysis
- **Professional HTML Reports**: Clean, print-ready competitive landscape grids
- **Real Logo Extraction**: Downloads and embeds actual brand logos
- **Color Palette Analysis**: Extracts dominant colors from website CSS
- **Brand Positioning Detection**: Identifies hero headlines and value propositions

### Multiple Analysis Tools
1. **Pure Live Grid Generator**: Zero fake data, only real extracted information
2. **Enhanced Brand Profiler**: Comprehensive brand analysis with AI insights
3. **Competitive Grid Generator**: Professional 5-row layout as specified
4. **Flask API**: RESTful endpoints for programmatic access

## 🎯 Quick Start

### Simple Grid Generation
```bash
python3 run_competitive_analysis.py
```

### With Custom URLs
```python
from pure_live_grid_generator import PureLiveGridGenerator

urls = ["https://your-urls.com"]
generator = PureLiveGridGenerator() 
html, data = generator.generate_pure_grid_html(urls)
```

## 📋 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/tom2tomtomtom/brand_audit.git
   cd brand_audit
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   export OPENAI_API_KEY="your_openai_api_key_here"
   ```

4. **Run analysis**
   ```bash
   python3 pure_live_grid_generator.py
   ```

## 🔧 Core Components

### Grid Generators
- `pure_live_grid_generator.py` - Zero placeholder data extraction
- `competitive_grid_generator.py` - Full-featured grid with web scraping
- `grid_html_generator.py` - Standalone HTML generator
- `run_competitive_analysis.py` - Easy-to-use interface

### Enhanced Analysis
- `enhanced_brand_profiler.py` - Comprehensive brand analysis
- `enhanced_report_generator.py` - Professional report generation
- `app.py` - Flask API server

### Legacy Tools
- `Project/` - Original competitor analysis scripts
- News article filtering and website content analysis

## 📊 Output Examples

The system generates professional competitive landscape grids with:

### 5-Row Structure
1. **Company Logos** - Real extracted logos or clean placeholders
2. **Brand Positioning** - Hero headlines and value propositions  
3. **Personality Descriptors** - AI-generated brand personality tags
4. **Color Palettes** - Extracted dominant colors from CSS
5. **Visual Assets** - Screenshots and brand material notes

### Real Data Extraction
- ✅ **Real Logos**: Downloaded and embedded as base64
- ✅ **Real Colors**: From actual website CSS/styles  
- ✅ **Real Positioning**: From hero sections and headlines
- ✅ **Real Brand Names**: From page content and metadata
- ❌ **Zero Placeholders**: Nothing fake or generated

## 🛠 API Endpoints

- `/api/enhanced-brand-audit` (POST): Generate comprehensive brand audit
- `/api/analyze-single-brand` (POST): Analyze individual brand
- `/api/generate-grid-preview` (POST): Generate grid preview
- `/scrape_competitor` (POST): Legacy competitor analysis
- `/filter_news` (GET): News article filtering

## 🎨 Technologies

### Backend
- Flask web framework
- OpenAI GPT-4 API
- Beautiful Soup for parsing
- Selenium for complex sites
- Pandas for data processing

### Analysis
- K-means clustering for color extraction
- Computer vision for logo detection
- Natural language processing for positioning
- Real-time web scraping

### Output
- Professional HTML/CSS grid layouts
- Base64 embedded images
- Print-ready formatting
- Responsive design

## 📈 Use Cases

- **Competitive Analysis**: Compare brand positioning across competitors
- **Brand Audits**: Analyze visual identity and messaging consistency  
- **Market Research**: Understand competitive landscape positioning
- **Strategy Planning**: Identify market gaps and opportunities
- **Client Presentations**: Professional competitive landscape reports

## 🔒 Data Privacy

- **No Persistent Storage**: Data is not saved permanently
- **Respectful Scraping**: Includes delays and rate limiting
- **Real Data Only**: No fake or generated placeholder content
- **Live Analysis**: Fresh data extracted on each run

## 🚀 Getting Started

1. **Run the simple generator**:
   ```bash
   python3 run_competitive_analysis.py
   ```

2. **Choose your analysis type**:
   - Financial Services
   - Tech Companies  
   - Custom URLs

3. **Get your HTML report** with real extracted data

The generated HTML file contains a professional competitive landscape grid with only real data extracted from live websites.
