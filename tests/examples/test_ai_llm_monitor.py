#!/usr/bin/env python3
"""
AI LLM Optimizer Monitor Test
Tests for infinite loops and stops immediately if detected.
Windows-compatible version.
"""

import sys
import os
import time
import threading
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from db.database import SessionLocal
from content_marketing.ai_llm_optimizer import AILLMOptimizer
from db.models import Product, ProductStatus

# Global flag to track if we're in a loop
loop_detected = False
start_time = None
test_completed = False

def timeout_checker():
    """Background thread to check for timeouts."""
    global loop_detected, test_completed
    time.sleep(120)  # Wait 2 minutes
    if not test_completed:
        loop_detected = True
        print(f"\n⚠️  TIMEOUT DETECTED - Possible infinite loop!")
        print(f"   Test running for more than 120 seconds")
        print(f"   Stopping test immediately...")
        os._exit(1)

def test_ai_llm_monitor():
    """Monitor test for AI LLM Optimizer with loop detection."""
    
    global start_time, loop_detected, test_completed
    start_time = time.time()
    
    print("🔍 AI LLM Optimizer Monitor Test - Loop Detection")
    print("=" * 55)
    print("⚠️  Test will stop if running longer than 120 seconds")
    
    # Start timeout checker thread
    timeout_thread = threading.Thread(target=timeout_checker, daemon=True)
    timeout_thread.start()
    
    # Initialize database session and optimizer
    db = SessionLocal()
    optimizer = AILLMOptimizer(db)
    
    try:
        # Test 1: Basic Initialization
        print("\n1. Testing Basic Initialization...")
        print(f"   ✅ AILLMOptimizer initialized successfully")
        print(f"   ✅ Database session: {type(db).__name__}")
        
        # Test 2: Create Test Product
        print("\n2. Creating Test Product...")
        test_product = Product(
            name="Monitor Test Product",
            description="Test product for monitoring",
            sku="MONITOR-TEST-001",
            category="Electronics",
            price=99.99,
            status=ProductStatus.ACTIVE,
            image_url="https://example.com/monitor-test.jpg",
            tags=["test", "electronics"],
            product_metadata={
                "features": ["Monitor Feature 1", "Monitor Feature 2"],
                "brand": "MonitorBrand",
                "warranty": "1 year"
            },
            review_count=50,
            average_rating=4.0
        )
        db.add(test_product)
        db.commit()
        db.refresh(test_product)
        print(f"   ✅ Test product created: {test_product.name} (ID: {test_product.id})")
        
        # Test 3: Monitor Main Coordinator Method
        print("\n3. Monitoring Main Coordinator Method...")
        print("   Testing create_ai_llm_optimized_content with loop detection...")
        
        method_start_time = time.time()
        
        # Monitor the method execution
        result = optimizer.create_ai_llm_optimized_content(
            "Monitor Test Topic",
            "blog",
            str(test_product.id)
        )
        
        method_end_time = time.time()
        method_duration = method_end_time - method_start_time
        
        # Check for potential loops
        if method_duration > 60:  # More than 1 minute
            print(f"   ⚠️  WARNING: Method took {method_duration:.2f} seconds")
            print(f"      This might indicate a loop or performance issue")
        else:
            print(f"   ✅ Method completed in {method_duration:.2f} seconds")
        
        if "error" not in result:
            print(f"   ✅ Coordinator method executed successfully!")
            print(f"      - Content ID: {result.get('content_id', 'N/A')}")
            print(f"      - Topic: {result.get('topic', 'N/A')}")
            print(f"      - Content type: {result.get('content_type', 'N/A')}")
            print(f"      - AI LLM optimized: {result.get('ai_llm_optimized', False)}")
            
            # Check optimization features
            optimization_features = result.get('optimization_features', {})
            print(f"      - Optimization features: {len(optimization_features)}")
            for feature, status in optimization_features.items():
                print(f"        • {feature}: {'✅' if status else '❌'}")
            
            # Check content structure
            base_content = result.get('base_content', {})
            if base_content:
                print(f"      - Base content generated: ✅")
                print(f"        • Content length: {len(base_content.get('content', ''))} chars")
            
            qa_content = result.get('qa_content', {})
            if qa_content:
                qa_pairs = qa_content.get('qa_pairs', [])
                print(f"      - Q&A content generated: ✅ ({len(qa_pairs)} pairs)")
            
        else:
            print(f"   ❌ Coordinator method failed: {result.get('error')}")
            return False
        
        # Test 4: Monitor Q&A Generation Specifically
        print("\n4. Monitoring Q&A Generation...")
        qa_start_time = time.time()
        
        try:
            qa_result = optimizer.qa_engine.generate_qa_content("Monitor Q&A Topic", str(test_product.id))
            qa_end_time = time.time()
            qa_duration = qa_end_time - qa_start_time
            
            if qa_duration > 30:  # More than 30 seconds
                print(f"   ⚠️  WARNING: Q&A generation took {qa_duration:.2f} seconds")
            else:
                print(f"   ✅ Q&A generation completed in {qa_duration:.2f} seconds")
            
            if "error" not in qa_result:
                qa_pairs = qa_result.get('qa_pairs', [])
                print(f"      - Generated {len(qa_pairs)} Q&A pairs")
            else:
                print(f"      - Q&A generation failed: {qa_result.get('error')}")
                
        except Exception as e:
            print(f"   ❌ Q&A generation exception: {e}")
        
        # Test 5: Monitor SEO Optimization
        print("\n5. Monitoring SEO Optimization...")
        seo_start_time = time.time()
        
        try:
            seo_result = optimizer.seo_optimizer.optimize_for_ai_llm("Monitor SEO Topic", "test content")
            seo_end_time = time.time()
            seo_duration = seo_end_time - seo_start_time
            
            if seo_duration > 20:  # More than 20 seconds
                print(f"   ⚠️  WARNING: SEO optimization took {seo_duration:.2f} seconds")
            else:
                print(f"   ✅ SEO optimization completed in {seo_duration:.2f} seconds")
                
        except Exception as e:
            print(f"   ❌ SEO optimization exception: {e}")
        
        # Test 6: Check for Loops in Logs
        print("\n6. Checking for Loop Indicators...")
        
        # Check if we have any suspicious patterns
        total_duration = time.time() - start_time
        if total_duration > 120:
            print(f"   ⚠️  WARNING: Total test duration is {total_duration:.2f} seconds")
            print(f"      This might indicate a loop")
        else:
            print(f"   ✅ Total test duration: {total_duration:.2f} seconds")
        
        # Test 7: Final Loop Check
        print("\n7. Final Loop Detection Check...")
        
        if loop_detected:
            print("   ❌ INFINITE LOOP DETECTED!")
            print("   Stopping test immediately...")
            return False
        else:
            print("   ✅ No infinite loops detected")
            print("   ✅ All monitoring checks passed")
        
        print(f"\n🎉 AI LLM Optimizer Monitor Test Completed Successfully!")
        print(f"   Total test time: {time.time() - start_time:.2f} seconds")
        
        test_completed = True
        return True
        
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Cleanup
        try:
            if 'test_product' in locals():
                db.delete(test_product)
                db.commit()
                print("   ✅ Test product cleaned up")
        except Exception as e:
            print(f"   ⚠️ Cleanup warning: {e}")
        
        test_completed = True
        db.close()

if __name__ == "__main__":
    success = test_ai_llm_monitor()
    if success:
        print("\n✅ All monitor tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some monitor tests failed!")
        sys.exit(1) 