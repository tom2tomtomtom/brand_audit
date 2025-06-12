"""
Brand Competitor Analysis Tool - Flask Backend
A comprehensive brand analysis tool that scrapes competitor websites,
analyzes brand elements, and generates professional PDF reports.
"""

from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import os
import json
import time
import threading
from datetime import datetime
from dotenv import load_dotenv
import logging

# Import our custom modules
from src.scraper import WebScraper
from src.analyzer import BrandAnalyzer
from src.report_generator import ReportGenerator
from src.progress_tracker import ProgressTracker

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global progress tracker
progress_tracker = ProgressTracker()

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')

@app.route('/debug/routes')
def debug_routes():
    """Debug endpoint to show all registered routes"""
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'rule': str(rule)
        })
    return jsonify(routes)

@app.route('/api/analyze', methods=['POST'])
def start_analysis():
    """Start a new brand analysis job"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'brands' not in data:
            return jsonify({'error': 'Missing brands data'}), 400
        
        brands = data['brands']
        if not isinstance(brands, list) or len(brands) < 3 or len(brands) > 5:
            return jsonify({'error': 'Must provide 3-5 brand URLs'}), 400
        
        # Validate URLs
        for brand in brands:
            if not isinstance(brand, str) or not brand.startswith(('http://', 'https://')):
                return jsonify({'error': f'Invalid URL: {brand}'}), 400
        
        # Create analysis job
        job_id = f"analysis_{int(time.time())}"
        
        # Initialize progress tracking
        progress_tracker.init_job(job_id, len(brands))
        
        # Start analysis in background thread
        analysis_thread = threading.Thread(
            target=run_analysis,
            args=(job_id, brands)
        )
        analysis_thread.daemon = True
        analysis_thread.start()
        
        return jsonify({
            'job_id': job_id,
            'status': 'started',
            'estimated_time': f'{len(brands) * 2}-{len(brands) * 3} minutes'
        })
        
    except Exception as e:
        logger.error(f"Error starting analysis: {str(e)}")
        return jsonify({'error': 'Failed to start analysis'}), 500

@app.route('/api/progress/<job_id>')
def get_progress(job_id):
    """Get current progress of an analysis job"""
    try:
        progress = progress_tracker.get_progress(job_id)
        if not progress:
            return jsonify({'error': 'Job not found'}), 404
        
        return jsonify(progress)
        
    except Exception as e:
        logger.error(f"Error getting progress: {str(e)}")
        return jsonify({'error': 'Failed to get progress'}), 500

@app.route('/api/result/<job_id>')
def get_result(job_id):
    """Get the completed analysis result"""
    try:
        result_file = f"results/{job_id}_report.pdf"
        
        if not os.path.exists(result_file):
            return jsonify({'error': 'Report not found'}), 404
        
        return send_file(
            result_file,
            as_attachment=True,
            download_name=f"brand_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        logger.error(f"Error getting result: {str(e)}")
        return jsonify({'error': 'Failed to get result'}), 500

def run_analysis(job_id, brands):
    """Run the complete brand analysis pipeline"""
    try:
        logger.info(f"Starting analysis job {job_id} for {len(brands)} brands")
        
        # Initialize components
        scraper = WebScraper()
        analyzer = BrandAnalyzer()
        report_generator = ReportGenerator()
        
        # Store scraped data for all brands
        all_brand_data = []
        
        # Step 1: Scrape all brands
        progress_tracker.update_progress(job_id, 0, "Initializing web scraper...")
        
        for i, brand_url in enumerate(brands):
            brand_name = extract_brand_name(brand_url)
            
            progress_tracker.update_progress(
                job_id, 
                (i / len(brands)) * 40,  # Scraping takes 40% of total time
                f"Scraping {brand_name}..."
            )
            
            # Scrape brand website - real timing from actual scraping
            brand_data = scraper.scrape_brand(brand_url, brand_name)
            all_brand_data.append(brand_data)
            
            # No artificial delays - actual scraping provides natural timing
        
        # Step 2: Analyze all brands
        progress_tracker.update_progress(job_id, 40, "Analyzing brand data with AI...")
        
        analysis_results = []
        for i, brand_data in enumerate(all_brand_data):
            progress_tracker.update_progress(
                job_id,
                40 + ((i / len(brands)) * 40),  # Analysis takes another 40%
                f"Analyzing {brand_data['name']} with AI..."
            )
            
            # Real AI analysis - timing depends on actual OpenAI API calls
            analysis = analyzer.analyze_brand(brand_data)
            analysis_results.append(analysis)
            
            # No artificial delays - actual AI analysis provides natural timing
        
        # Step 3: Generate comparative analysis
        progress_tracker.update_progress(job_id, 80, "Generating competitive insights...")
        
        comparative_analysis = analyzer.generate_comparative_analysis(analysis_results)
        
        # Step 4: Generate PDF report
        progress_tracker.update_progress(job_id, 90, "Creating PDF report...")
        
        # Ensure results directory exists
        os.makedirs("results", exist_ok=True)
        
        report_path = f"results/{job_id}_report.pdf"
        report_generator.generate_report(
            all_brand_data,
            analysis_results,
            comparative_analysis,
            report_path
        )
        
        # Complete the job
        progress_tracker.complete_job(job_id, report_path)
        
        logger.info(f"Analysis job {job_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Analysis job {job_id} failed: {str(e)}")
        progress_tracker.fail_job(job_id, str(e))

def extract_brand_name(url):
    """Extract brand name from URL"""
    try:
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        domain = domain.replace('www.', '')
        brand_name = domain.split('.')[0]
        return brand_name.title()
    except:
        return "Unknown Brand"

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs("results", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    os.makedirs("src", exist_ok=True)
    
    # Get port from environment (Railway uses PORT env var)
    port = int(os.environ.get('PORT', 5000))
    
    # Run the Flask app
    app.run(debug=False, host='0.0.0.0', port=port)