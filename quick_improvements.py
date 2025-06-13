#!/usr/bin/env python3
"""
Quick improvements for the competitive intelligence system
These can be implemented in 1-2 hours each
"""

import hashlib
import pickle
import os
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, Any, Optional

class QuickImprovements:
    """Easy-to-implement enhancements"""
    
    def __init__(self):
        self.cache_dir = "/tmp/competitive_intel_cache"
        os.makedirs(self.cache_dir, exist_ok=True)
    
    # 1. SIMPLE CACHING (30 minutes)
    def get_cached_analysis(self, url: str) -> Optional[Dict[str, Any]]:
        """Check if we have recent analysis for this URL"""
        cache_key = hashlib.md5(url.encode()).hexdigest()
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'rb') as f:
                    data, timestamp = pickle.load(f)
                    age = datetime.now() - timestamp
                    if age < timedelta(hours=2):  # 2 hour cache
                        print(f"✅ Using cached data for {url} (age: {age})")
                        return data
            except:
                pass
        return None
    
    def save_to_cache(self, url: str, data: Dict[str, Any]):
        """Save analysis to cache"""
        cache_key = hashlib.md5(url.encode()).hexdigest()
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
        
        with open(cache_file, 'wb') as f:
            pickle.dump((data, datetime.now()), f)
    
    # 2. PROGRESS TRACKING (20 minutes)
    class ProgressTracker:
        def __init__(self, total_steps: int, callback=None):
            self.total = total_steps
            self.current = 0
            self.callback = callback
            
        def update(self, message: str):
            self.current += 1
            percent = int((self.current / self.total) * 100)
            print(f"[{percent}%] {message}")
            if self.callback:
                self.callback(message, percent)
    
    # 3. CSV EXPORT (15 minutes)
    def export_competitive_data_csv(self, competitive_data: Dict[str, Any]) -> str:
        """Export competitive analysis to CSV"""
        rows = []
        
        for brand in competitive_data.get('competitors', []):
            row = {
                'Company': brand.get('company_name', ''),
                'URL': brand.get('url', ''),
                'Industry': brand.get('industry', ''),
                'Positioning': brand.get('market_position', ''),
                'Key Differentiators': ', '.join(brand.get('differentiators', [])),
                'Main Products': ', '.join(brand.get('products', [])),
                'Brand Score': brand.get('brand_score', 0),
                'Primary Colors': ', '.join(brand.get('colors', [])),
                'Market Segment': brand.get('target_market', ''),
                'Strengths': ', '.join([s for s in brand.get('swot', {}).get('strengths', [])]),
                'Weaknesses': ', '.join([w for w in brand.get('swot', {}).get('weaknesses', [])])
            }
            rows.append(row)
        
        df = pd.DataFrame(rows)
        return df.to_csv(index=False)
    
    # 4. RETRY LOGIC (10 minutes)
    def retry_on_failure(self, func, max_attempts=3, delay=2):
        """Simple retry wrapper"""
        for attempt in range(max_attempts):
            try:
                return func()
            except Exception as e:
                if attempt < max_attempts - 1:
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                    time.sleep(delay * (attempt + 1))  # Exponential backoff
                else:
                    raise
    
    # 5. BASIC PERFORMANCE METRICS (20 minutes)
    def add_performance_tracking(self, start_time: datetime) -> Dict[str, Any]:
        """Track performance metrics"""
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        return {
            'analysis_duration_seconds': duration,
            'analysis_duration_formatted': f"{int(duration // 60)}m {int(duration % 60)}s",
            'timestamp': end_time.isoformat(),
            'cached_urls_used': self.cache_stats.get('hits', 0),
            'new_urls_analyzed': self.cache_stats.get('misses', 0)
        }

# Example integration:
"""
# In strategic_competitive_intelligence.py:

from quick_improvements import QuickImprovements

class StrategicCompetitiveIntelligence:
    def __init__(self):
        self.improvements = QuickImprovements()
        self.progress = None
    
    def analyze_brand(self, url):
        # Check cache first
        cached = self.improvements.get_cached_analysis(url)
        if cached:
            return cached
        
        # Track progress
        if self.progress:
            self.progress.update(f"Analyzing {url}")
        
        # Do analysis...
        result = self._perform_analysis(url)
        
        # Save to cache
        self.improvements.save_to_cache(url, result)
        
        return result
"""