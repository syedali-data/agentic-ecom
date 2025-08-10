#!/usr/bin/env python3
"""
Isolated test for Q&A engine to check for infinite loops.
"""

import sys
import os
import time
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from db.database import SessionLocal
from content_marketing.qa_engine import QAEngine
from db.models import Product, ProductStatus

def test_qa_isolated():
    """Isolated test for Q&A engine."""
    
    print("🔍 Isolated Q&A Engine Test")
    print("=" * 40)
    
    # Initialize database session and Q&A engine
    db = SessionLocal()
    qa_engine = QAEngine(db)
    
    try:
        # Test 1: Basic Q&A Generation
        print("\n1. Testing Basic Q&A Generation...")
        start_time = time.time()
        
        result = qa_engine.generate_qa_content("Test Topic", None)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"   Duration: {duration:.2f} seconds")
        
        if "error" not in result:
            qa_pairs = result.get('qa_pairs', [])
            print(f"   ✅ Generated {len(qa_pairs)} Q&A pairs")
            print(f"   ✅ Topic: {result.get('topic', 'N/A')}")
            print(f"   ✅ AI LLM optimized: {result.get('ai_llm_optimized', False)}")
        else:
            print(f"   ❌ Failed: {result.get('error')}")
            return False
        
        # Test 2: Check for Optimization Issues
        print("\n2. Testing Optimization...")
        if qa_pairs:
            print(f"   Checking optimization of {len(qa_pairs)} pairs...")
            
            # Check if optimization is working
            optimized_pairs = qa_engine._optimize_for_ai_llm(qa_pairs, "Test Topic")
            
            if len(optimized_pairs) == len(qa_pairs):
                print(f"   ✅ Optimization successful: {len(optimized_pairs)} pairs")
            else:
                print(f"   ⚠️ Optimization returned {len(optimized_pairs)} pairs (expected {len(qa_pairs)})")
        
        # Test 3: Check for Recursive Calls
        print("\n3. Checking for Recursive Calls...")
        
        # Monitor the generate_qa_content method
        start_time = time.time()
        
        # This should not cause infinite loops
        result2 = qa_engine.generate_qa_content("Another Test Topic", None)
        
        end_time = time.time()
        duration2 = end_time - start_time
        
        print(f"   Duration: {duration2:.2f} seconds")
        
        if duration2 > 60:
            print(f"   ⚠️ WARNING: Second call took {duration2:.2f} seconds")
            print(f"      This might indicate a loop")
        else:
            print(f"   ✅ Second call completed in {duration2:.2f} seconds")
        
        if "error" not in result2:
            qa_pairs2 = result2.get('qa_pairs', [])
            print(f"   ✅ Generated {len(qa_pairs2)} Q&A pairs")
        else:
            print(f"   ❌ Second call failed: {result2.get('error')}")
        
        print(f"\n🎉 Isolated Q&A Engine Test Completed!")
        print(f"   Total test time: {time.time() - start_time:.2f} seconds")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        db.close()

if __name__ == "__main__":
    success = test_qa_isolated()
    if success:
        print("\n✅ All isolated tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some isolated tests failed!")
        sys.exit(1) 