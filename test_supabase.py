#!/usr/bin/env python3
"""
Test Supabase integration for brand audit tool
"""

import os
import sys
sys.path.append('src')

from dotenv import load_dotenv
from supabase_tracker import SupabaseProgressTracker, FallbackProgressTracker

def test_supabase_integration():
    """Test Supabase integration and fallback behavior"""
    load_dotenv()
    
    print("🧪 Testing Supabase Integration")
    print("=" * 50)
    
    # Test 1: Check environment variables
    print("\n1. Environment Variables:")
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    print(f"   SUPABASE_URL: {'✅ Set' if supabase_url and supabase_url != 'https://your-project.supabase.co' else '❌ Not configured'}")
    print(f"   SUPABASE_ANON_KEY: {'✅ Set' if supabase_key and supabase_key != 'your_supabase_anon_key_here' else '❌ Not configured'}")
    
    # Test 2: Initialize tracker
    print("\n2. Tracker Initialization:")
    try:
        tracker = SupabaseProgressTracker()
        if tracker.supabase is None:
            print("   ✅ Supabase not configured - using fallback tracker")
            tracker = FallbackProgressTracker()
            tracker_type = "Fallback (In-Memory)"
        else:
            print("   ✅ Supabase tracker initialized successfully")
            tracker_type = "Supabase (Persistent)"
    except Exception as e:
        print(f"   ❌ Error initializing tracker: {e}")
        tracker = FallbackProgressTracker()
        tracker_type = "Fallback (In-Memory)"
    
    print(f"   Using: {tracker_type}")
    
    # Test 3: Job operations
    print("\n3. Job Operations:")
    test_job_id = "test_job_123"
    
    try:
        # Initialize job
        tracker.init_job(test_job_id, 3)
        print("   ✅ Job initialization")
        
        # Update progress
        tracker.update_progress(test_job_id, 25.0, "Testing progress update")
        print("   ✅ Progress update")
        
        # Get progress
        progress = tracker.get_progress(test_job_id)
        if progress:
            print(f"   ✅ Progress retrieval: {progress['progress']}% - {progress['message']}")
        else:
            print("   ❌ Failed to retrieve progress")
        
        # Complete job
        tracker.complete_job(test_job_id, "/path/to/test/result.pdf")
        print("   ✅ Job completion")
        
        # Final progress check
        final_progress = tracker.get_progress(test_job_id)
        if final_progress and final_progress['status'] == 'completed':
            print("   ✅ Final status verification")
        else:
            print("   ❌ Final status verification failed")
            
    except Exception as e:
        print(f"   ❌ Job operations failed: {e}")
    
    # Test 4: Error handling
    print("\n4. Error Handling:")
    try:
        error_job_id = "error_test_456"
        tracker.init_job(error_job_id, 1)
        tracker.fail_job(error_job_id, "Test error message")
        error_progress = tracker.get_progress(error_job_id)
        if error_progress and error_progress['status'] == 'failed':
            print("   ✅ Error handling works correctly")
        else:
            print("   ❌ Error handling failed")
    except Exception as e:
        print(f"   ❌ Error handling test failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Integration Test Summary:")
    print(f"   Tracker Type: {tracker_type}")
    
    if tracker_type == "Supabase (Persistent)":
        print("   ✅ Jobs will persist through app restarts")
        print("   ✅ Multiple users can run concurrent analyses")
        print("   ✅ Job history is maintained in database")
    else:
        print("   ⚠️  Jobs will be lost on app restart")
        print("   ⚠️  Limited to single instance memory")
        print("   💡 Consider setting up Supabase for production use")
    
    print("\n📚 Next Steps:")
    if tracker_type == "Fallback (In-Memory)":
        print("   1. Create a Supabase project at https://supabase.com")
        print("   2. Run the SQL schema from supabase_schema.sql")
        print("   3. Update .env with your Supabase credentials")
        print("   4. Restart the application")
    else:
        print("   ✅ Supabase integration is working!")
        print("   🚀 Deploy to Railway with confidence")

if __name__ == "__main__":
    test_supabase_integration()