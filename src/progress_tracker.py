"""
Progress Tracker Module
Tracks and manages progress of analysis jobs
"""

import time
import threading
from typing import Dict, Optional

class ProgressTracker:
    def __init__(self):
        """Initialize the progress tracker"""
        self.jobs = {}
        self.lock = threading.Lock()
    
    def init_job(self, job_id: str, total_brands: int):
        """Initialize a new analysis job"""
        with self.lock:
            self.jobs[job_id] = {
                'status': 'started',
                'progress': 0,
                'message': 'Initializing analysis...',
                'total_brands': total_brands,
                'current_brand': 0,
                'started_at': time.time(),
                'estimated_completion': None,
                'result_path': None,
                'error': None
            }
    
    def update_progress(self, job_id: str, progress: float, message: str):
        """Update job progress"""
        with self.lock:
            if job_id in self.jobs:
                self.jobs[job_id]['progress'] = min(100, max(0, progress))
                self.jobs[job_id]['message'] = message
                self.jobs[job_id]['last_updated'] = time.time()
                
                # Estimate completion time
                elapsed = time.time() - self.jobs[job_id]['started_at']
                if progress > 0:
                    total_estimated = (elapsed / progress) * 100
                    remaining = total_estimated - elapsed
                    self.jobs[job_id]['estimated_completion'] = remaining
    
    def complete_job(self, job_id: str, result_path: str):
        """Mark job as completed"""
        with self.lock:
            if job_id in self.jobs:
                self.jobs[job_id]['status'] = 'completed'
                self.jobs[job_id]['progress'] = 100
                self.jobs[job_id]['message'] = 'Analysis completed successfully'
                self.jobs[job_id]['result_path'] = result_path
                self.jobs[job_id]['completed_at'] = time.time()
    
    def fail_job(self, job_id: str, error_message: str):
        """Mark job as failed"""
        with self.lock:
            if job_id in self.jobs:
                self.jobs[job_id]['status'] = 'failed'
                self.jobs[job_id]['message'] = f'Analysis failed: {error_message}'
                self.jobs[job_id]['error'] = error_message
                self.jobs[job_id]['failed_at'] = time.time()
    
    def get_progress(self, job_id: str) -> Optional[Dict]:
        """Get current progress of a job"""
        with self.lock:
            if job_id not in self.jobs:
                return None
            
            job = self.jobs[job_id].copy()
            
            # Add human-readable time estimates
            if job.get('estimated_completion'):
                remaining_seconds = int(job['estimated_completion'])
                if remaining_seconds > 0:
                    minutes = remaining_seconds // 60
                    seconds = remaining_seconds % 60
                    job['estimated_time_remaining'] = f"{minutes}m {seconds}s"
                else:
                    job['estimated_time_remaining'] = "Almost done"
            
            return job
    
    def cleanup_old_jobs(self, max_age_hours: int = 24):
        """Clean up old completed/failed jobs"""
        with self.lock:
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            
            jobs_to_remove = []
            for job_id, job_data in self.jobs.items():
                if job_data['status'] in ['completed', 'failed']:
                    job_age = current_time - job_data.get('completed_at', job_data.get('failed_at', current_time))
                    if job_age > max_age_seconds:
                        jobs_to_remove.append(job_id)
            
            for job_id in jobs_to_remove:
                del self.jobs[job_id]