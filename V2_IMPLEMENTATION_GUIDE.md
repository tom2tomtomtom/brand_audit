# Brand Audit V2 Implementation Guide

## Overview

The V2 implementation represents a complete overhaul of the brand analysis system with these core principles:

1. **Real Data Only** - No fallbacks, no placeholders, no synthetic data
2. **Industry Agnostic** - Dynamic industry detection instead of hardcoded assumptions
3. **Multi-Strategy Extraction** - Multiple methods to handle modern websites
4. **Intelligent Validation** - Quality scoring and validation without defaults

## Key Improvements Implemented

### 1. Zero Tolerance for Fake Data
- ❌ All default/fallback methods removed
- ✅ Returns `None` or error status when extraction fails
- ✅ Transparent failure reporting with reasons

### 2. Multi-Strategy Content Extraction
```python
# Extraction strategies in order:
1. BeautifulSoup (fast, works for static sites)
2. Selenium (handles JavaScript rendering)
3. Playwright (modern SPA support)
```

### 3. Intelligent Content Processing
- No truncation - processes full content
- Extracts semantic structure (headings, navigation, main content)
- Preserves context for better AI analysis

### 4. Adaptive AI Analysis
- **Dynamic Industry Detection** - Identifies industry from content
- **Model Selection** - Chooses GPT-4, GPT-4o, or GPT-4o-mini based on complexity
- **Retry Logic** - 3 different prompt strategies (detailed → simplified → guided)

### 5. Structured Output with Validation
- Uses OpenAI function calling for guaranteed structure
- Confidence scores for each extracted field
- Validation against original content

### 6. Enhanced Visual Extraction
- Multiple methods for logo detection
- Color extraction from CSS, screenshots, and SVGs
- Intelligent clustering for color palettes

## Architecture

```
CompetitiveGridGeneratorV2
│
├── EnhancedBrandProfilerV2
│   ├── extract_with_fallbacks()
│   │   ├── extract_with_beautifulsoup()
│   │   ├── extract_with_selenium()
│   │   └── extract_with_playwright()
│   │
│   ├── intelligent_content_extraction()
│   │   ├── extract_all_headings()
│   │   ├── extract_navigation_tree()
│   │   ├── extract_main_content_blocks()
│   │   ├── extract_json_ld()
│   │   └── extract_semantic_html5()
│   │
│   ├── extract_with_retry()
│   │   ├── detect_industry_context()
│   │   ├── detailed_extraction_prompt()
│   │   ├── simplified_extraction_prompt()
│   │   └── guided_extraction_prompt()
│   │
│   └── extract_visual_elements()
│       ├── extract_from_computed_styles()
│       ├── analyze_screenshot_colors()
│       ├── extract_svg_colors()
│       └── extract_logos_comprehensive()
│
└── generate_grid_html()
    ├── _generate_extraction_summary()
    ├── _generate_grid_content()
    └── _generate_failed_extractions_section()
```

## Usage

### Basic Usage

```python
from competitive_grid_generator_v2 import CompetitiveGridGeneratorV2

# Initialize generator
generator = CompetitiveGridGeneratorV2()

# Analyze brands
urls = [
    "https://www.stripe.com",
    "https://www.shopify.com",
    "https://www.square.com"
]

# Generate report
result = generator.generate_report(
    urls=urls,
    report_title="Payment Platforms Analysis",
    output_filename="payment_analysis.html"
)
```

### Advanced Usage with Custom Analysis

```python
from enhanced_brand_profiler_v2 import EnhancedBrandProfilerV2

# Direct brand analysis
profiler = EnhancedBrandProfilerV2()
profile = profiler.analyze_brand("https://www.example.com")

if profile['status'] == 'success':
    print(f"Company: {profile['brand_data']['company_name']}")
    print(f"Quality Score: {profile['extraction_quality']:.2f}")
    print(f"Extraction Method: {profile['extraction_method']}")
else:
    print(f"Failed: {profile['error']}")
```

## Output Format

### Successful Extraction
```json
{
  "status": "success",
  "url": "https://example.com",
  "extraction_method": "selenium",
  "brand_data": {
    "company_name": "Example Corp",
    "brand_positioning": "Leading solution for...",
    "key_messages": ["Message 1", "Message 2"],
    "target_audience": "Small businesses",
    "brand_personality": ["Innovative", "Reliable"],
    "confidence_scores": {
      "company_name": 0.95,
      "positioning": 0.85,
      "overall": 0.90
    }
  },
  "visual_data": {
    "css_extraction": ["#FF5733", "#1E90FF"],
    "logo_extraction": ["https://example.com/logo.png"]
  },
  "extraction_quality": 0.87
}
```

### Failed Extraction
```json
{
  "status": "failed",
  "url": "https://example.com",
  "error": "No content could be extracted",
  "extracted_data": null
}
```

## Quality Indicators

The system provides quality scores at multiple levels:

1. **Field-Level Confidence** (0-1)
   - Per-field confidence scores
   - Based on clarity and context

2. **Extraction Quality** (0-1)
   - Overall quality score
   - Considers completeness and validity

3. **Visual Quality Classes**
   - `quality-high`: Score ≥ 0.8
   - `quality-medium`: Score ≥ 0.5
   - `quality-low`: Score < 0.5

## Error Handling

The system provides detailed error information:

```python
# Extraction failures are tracked
failed_extractions = [
  {
    "url": "https://blocked-site.com",
    "reason": "Connection timeout"
  },
  {
    "url": "https://requires-auth.com",
    "reason": "Authentication required"
  }
]
```

## Best Practices

1. **URL Preparation**
   - Use full URLs with protocol (https://)
   - Ensure sites are publicly accessible
   - Avoid sites requiring authentication

2. **Batch Processing**
   - Process 5-10 URLs at a time for best results
   - Monitor extraction success rates
   - Review failed extractions for patterns

3. **Quality Assurance**
   - Check extraction quality scores
   - Validate critical data manually
   - Use confidence scores to prioritize review

## Troubleshooting

### Common Issues

1. **Low Extraction Success Rate**
   - Check if sites require authentication
   - Verify URLs are correct and accessible
   - Some SPAs may need more wait time

2. **Low Quality Scores**
   - Minimal content websites
   - Non-standard HTML structure
   - Heavy JavaScript frameworks

3. **Missing Visual Data**
   - Sites blocking screenshots
   - SVG-only logos
   - CSS-in-JS implementations

### Debug Mode

Enable verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Performance Considerations

- **BeautifulSoup**: ~1-2 seconds per site
- **Selenium**: ~5-10 seconds per site
- **Playwright**: ~5-8 seconds per site
- **AI Analysis**: ~2-5 seconds per site

Total: ~10-20 seconds per brand for full analysis

## Future Enhancements

Potential areas for improvement:
1. Parallel processing for multiple URLs
2. Caching for repeated analyses
3. WebSocket support for real-time updates
4. API rate limiting and retry logic
5. Enhanced screenshot analysis with OCR
