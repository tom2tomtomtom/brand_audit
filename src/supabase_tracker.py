"""
Supabase Progress Tracker Module
Replaces in-memory progress tracking with persistent database storage
"""

import time
import json
import logging
from typing import Dict, Optional, List
from supabase import create_client, Client
import os

logger = logging.getLogger(__name__)

class SupabaseProgressTracker:
    def __init__(self):
        """Initialize Supabase client"""
        self.supabase: Optional[Client] = None
        self.setup_client()
    
    def setup_client(self):
        """Setup Supabase client with environment variables"""
        try:
            supabase_url = os.getenv('SUPABASE_URL')
            supabase_key = os.getenv('SUPABASE_ANON_KEY')
            
            if not supabase_url or not supabase_key:
                logger.warning("Supabase credentials not found, falling back to in-memory storage")
                return
            
            self.supabase = create_client(supabase_url, supabase_key)
            logger.info("Supabase client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {str(e)}")
    
    def init_job(self, job_id: str, total_brands: int):
        """Initialize a new analysis job in Supabase"""
        if not self.supabase:
            logger.warning("Supabase not available, cannot persist job")
            return
        
        try:
            job_data = {
                'job_id': job_id,
                'status': 'started',
                'progress': 0.0,
                'current_task': 'Initializing analysis...',
                'total_brands': total_brands,
                'created_at': 'now()',
                'updated_at': 'now()'
            }
            
            result = self.supabase.table('analysis_jobs').insert(job_data).execute()
            logger.info(f"Job {job_id} initialized in Supabase")
            
        except Exception as e:
            logger.error(f"Failed to initialize job in Supabase: {str(e)}")
    
    def update_progress(self, job_id: str, progress: float, message: str):
        """Update job progress in Supabase"""
        if not self.supabase:
            return
        
        try:
            update_data = {
                'progress': min(100.0, max(0.0, progress)),
                'current_task': message,
                'updated_at': 'now()'
            }
            
            # Calculate estimated completion time
            if progress > 0:
                # Get job start time
                job_result = self.supabase.table('analysis_jobs')\
                    .select('created_at')\
                    .eq('job_id', job_id)\
                    .execute()
                
                if job_result.data:
                    # This is a simplified estimation - could be more sophisticated
                    estimated_total_seconds = (100 / progress) * 300  # Rough estimate
                    update_data['estimated_completion'] = int(estimated_total_seconds)
            
            result = self.supabase.table('analysis_jobs')\
                .update(update_data)\
                .eq('job_id', job_id)\
                .execute()
            
            logger.info(f"Progress updated for job {job_id}: {progress}%")
            
        except Exception as e:
            logger.error(f"Failed to update progress in Supabase: {str(e)}")
    
    def complete_job(self, job_id: str, result_path: str):
        """Mark job as completed in Supabase"""
        if not self.supabase:
            return
        
        try:
            update_data = {
                'status': 'completed',
                'progress': 100.0,
                'current_task': 'Analysis completed',
                'result_file_path': result_path,
                'completed_at': 'now()',
                'updated_at': 'now()'
            }
            
            result = self.supabase.table('analysis_jobs')\
                .update(update_data)\
                .eq('job_id', job_id)\
                .execute()
            
            logger.info(f"Job {job_id} marked as completed")
            
        except Exception as e:
            logger.error(f"Failed to complete job in Supabase: {str(e)}")
    
    def fail_job(self, job_id: str, error_message: str):
        """Mark job as failed in Supabase"""
        if not self.supabase:
            return
        
        try:
            update_data = {
                'status': 'failed',
                'error_message': error_message,
                'updated_at': 'now()'
            }
            
            result = self.supabase.table('analysis_jobs')\
                .update(update_data)\
                .eq('job_id', job_id)\
                .execute()
            
            logger.info(f"Job {job_id} marked as failed: {error_message}")
            
        except Exception as e:
            logger.error(f"Failed to fail job in Supabase: {str(e)}")
    
    def get_progress(self, job_id: str) -> Optional[Dict]:
        """Get current progress of a job from Supabase"""
        if not self.supabase:
            return None
        
        try:
            result = self.supabase.table('analysis_jobs')\
                .select('*')\
                .eq('job_id', job_id)\
                .execute()
            
            if not result.data:
                logger.warning(f"Job {job_id} not found in Supabase")
                return None
            
            job_data = result.data[0]
            
            # Format the response to match expected format
            progress_data = {
                'status': job_data['status'],
                'progress': float(job_data['progress']),
                'message': job_data['current_task'],
                'total_brands': job_data.get('total_brands', 0),
                'estimated_completion': job_data.get('estimated_completion'),
                'error': job_data.get('error_message'),
                'result_path': job_data.get('result_file_path')
            }
            
            return progress_data
            
        except Exception as e:
            logger.error(f"Failed to get progress from Supabase: {str(e)}")
            return None
    
    def get_active_jobs(self) -> List[str]:
        """Get list of active job IDs"""
        if not self.supabase:
            return []
        
        try:
            result = self.supabase.table('analysis_jobs')\
                .select('job_id')\
                .in_('status', ['started', 'running'])\
                .execute()
            
            return [job['job_id'] for job in result.data]
            
        except Exception as e:
            logger.error(f"Failed to get active jobs: {str(e)}")
            return []
    
    def cleanup_old_jobs(self, days_old: int = 7):
        """Clean up jobs older than specified days"""
        if not self.supabase:
            return
        
        try:
            # Delete jobs older than specified days
            result = self.supabase.table('analysis_jobs')\
                .delete()\
                .lt('created_at', f'now() - interval \'{days_old} days\'')\
                .execute()
            
            logger.info(f"Cleaned up old jobs: {len(result.data) if result.data else 0} deleted")
            
        except Exception as e:
            logger.error(f"Failed to cleanup old jobs: {str(e)}")

# Fallback to in-memory tracker if Supabase fails
class FallbackProgressTracker:
    def __init__(self):
        """Fallback in-memory progress tracker"""
        self.jobs = {}
        logger.warning("Using fallback in-memory progress tracker")
    
    def init_job(self, job_id: str, total_brands: int):
        self.jobs[job_id] = {
            'status': 'started',
            'progress': 0,
            'message': 'Initializing analysis...',
            'total_brands': total_brands,
            'started_at': time.time()
        }
    
    def update_progress(self, job_id: str, progress: float, message: str):
        if job_id in self.jobs:
            self.jobs[job_id]['progress'] = progress
            self.jobs[job_id]['message'] = message
    
    def complete_job(self, job_id: str, result_path: str):
        if job_id in self.jobs:
            self.jobs[job_id]['status'] = 'completed'
            self.jobs[job_id]['result_path'] = result_path
    
    def fail_job(self, job_id: str, error_message: str):
        if job_id in self.jobs:
            self.jobs[job_id]['status'] = 'failed'
            self.jobs[job_id]['error'] = error_message
    
    def get_progress(self, job_id: str) -> Optional[Dict]:
        return self.jobs.get(job_id)
    
    def get_active_jobs(self) -> List[str]:
        return list(self.jobs.keys())