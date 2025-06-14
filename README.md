# Brand Competitor Analysis & Grid Generator V2

A comprehensive brand analysis platform that scrapes competitor websites, analyzes brand elements, and generates professional competitive landscape reports. **Version 2 features real data only extraction with no fallbacks or synthetic data.**

## 🚀 What's New in V2

### Core Improvements
- **🚫 Zero Fallback Data**: No placeholders, defaults, or synthetic content - only real extracted data
- **🌐 Industry Agnostic**: Dynamic industry detection instead of hardcoded assumptions  
- **🔄 Multi-Strategy Extraction**: BeautifulSoup → Selenium → Playwright fallback chain
- **🎯 Intelligent Validation**: Quality scoring and confidence metrics for all extractions
- **🤖 Adaptive AI Analysis**: Dynamic model selection (GPT-4/GPT-4o/GPT-4o-mini) based on complexity

## 🎯 Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/tom2tomtomtom/brand_audit.git
cd brand_audit

# Install V2 requirements
pip install -r requirements_v2.txt

# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"
```

### Quick Analysis
```bash
# Interactive quick start
python quick_start_v2.py

# Comprehensive demo
python demo_v2_comprehensive.py

# Direct usage
python competitive_grid_generator_v2.py
```

## 📋 Features

### V2 Extraction Capabilities
- **Multi-Method Content Extraction**
  - Static HTML parsing (BeautifulSoup)
  - JavaScript rendering (Selenium)
  - Modern SPA support (Playwright)
  
- **Intelligent Content Analysis**  
  - Semantic HTML5 structure detection
  - Navigation tree extraction
  - JSON-LD structured data parsing
  - Meta tag comprehensive analysis

- **Visual Element Extraction**
  - Logo detection with multiple strategies
  - Color palette from CSS/screenshots/SVGs
  - Visual style analysis

- **Quality Assurance**
  - Field-level confidence scores (0-1)
  - Overall extraction quality metrics
  - Validation against source content
  - Transparent failure reporting

## 🔧 Core V2 Components

### Enhanced Brand Profiler V2
```python
from enhanced_brand_profiler_v2 import EnhancedBrandProfilerV2

profiler = EnhancedBrandProfilerV2()
profile = profiler.analyze_brand("https://example.com")

if profile['status'] == 'success':
    print(f"Company: {profile['brand_data']['company_name']}")
    print(f"Quality: {profile['extraction_quality']:.2f}")
else:
    print(f"Failed: {profile['error']}")
```

### Competitive Grid Generator V2
```python
from competitive_grid_generator_v2 import CompetitiveGridGeneratorV2

generator = CompetitiveGridGeneratorV2()
result = generator.generate_report(
    urls=["https://stripe.com", "https://square.com"],
    report_title="Payment Platform Analysis"
)
```

## 📊 Output Examples

### V2 Grid Structure
The system generates professional competitive landscape grids with:

1. **Company Logos** - Real extracted logos with confidence scores
2. **Brand Positioning** - Actual headlines and value propositions  
3. **Personality Descriptors** - AI-analyzed brand traits
4. **Color Palettes** - Extracted dominant colors
5. **Visual Style** - Design characteristics

### Real Data Indicators
- ✅ **Quality Badges**: High/Medium/Low extraction quality
- 📊 **Confidence Scores**: Per-field reliability metrics
- ❌ **Failed Extractions**: Clear reporting of what couldn't be extracted

## 🛠 V2 API

### Response Format
```json
{
  "status": "success|failed",
  "url": "https://example.com",
  "extraction_method": "selenium",
  "brand_data": {
    "company_name": "Example Corp",
    "brand_positioning": "Leading solution for...",
    "confidence_scores": {
      "company_name": 0.95,
      "positioning": 0.85
    }
  },
  "visual_data": {
    "logo_extraction": ["url1", "url2"],
    "css_extraction": ["#FF5733", "#1E90FF"]
  },
  "extraction_quality": 0.87
}
```

## 🎨 Use Cases

- **Competitive Analysis**: Compare real brand positioning
- **Market Research**: Understand actual competitive landscapes
- **Brand Audits**: Analyze consistency with extracted data
- **Strategy Planning**: Identify gaps based on real content
- **Client Presentations**: Show actual competitor positioning

## 🔒 Ethical Considerations

- **Respectful Scraping**: Includes delays and rate limiting
- **Public Data Only**: Analyzes only publicly accessible content
- **No Data Storage**: Real-time analysis without persistence
- **Transparent Methods**: Clear indication of extraction methods

## 📈 Performance

- **BeautifulSoup**: ~1-2 seconds (static sites)
- **Selenium**: ~5-10 seconds (JavaScript sites)  
- **Playwright**: ~5-8 seconds (modern SPAs)
- **AI Analysis**: ~2-5 seconds
- **Total**: ~10-20 seconds per brand

## 🚀 Getting Started

1. **Run the quick start**:
   ```bash
   python quick_start_v2.py
   ```

2. **Try the comprehensive demo**:
   ```bash
   python demo_v2_comprehensive.py
   ```

3. **Read the implementation guide**:
   - [V2_IMPLEMENTATION_GUIDE.md](V2_IMPLEMENTATION_GUIDE.md)

## 🤝 Contributing

We welcome contributions! The V2 system prioritizes:
- Real data extraction improvements
- Additional extraction strategies
- Better validation methods
- Performance optimizations

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- Beautiful Soup, Selenium, Playwright teams
- Contributors to the extraction strategies

---

**Note**: This is V2 of the Brand Audit system. For the legacy version with fallback data, see the v1 branch.
