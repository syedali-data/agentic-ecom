#!/usr/bin/env python3
"""
Simple test for AI LLM Optimizer - Q&A content type only.
"""

import sys
import os
import time
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from db.database import SessionLocal
from content_marketing.ai_llm_optimizer import AILLMOptimizer
from db.models import Product, ProductStatus

def test_ai_llm_simple():
    """Simple test for AI LLM Optimizer."""
    
    print("🔍 Simple AI LLM Optimizer Test - Q&A Content Type")
    print("=" * 55)
    
    # Initialize database session and optimizer
    db = SessionLocal()
    optimizer = AILLMOptimizer(db)
    
    try:
        # Test 1: Create Test Product
        print("\n1. Creating Test Product...")
        test_product = Product(
            name="Simple Test Product",
            description="Test product for simple test",
            sku="SIMPLE-TEST-001",
            category="Electronics",
            price=99.99,
            status=ProductStatus.ACTIVE,
            image_url="https://example.com/simple-test.jpg",
            tags=["test", "electronics"],
            product_metadata={
                "features": ["Simple Feature 1", "Simple Feature 2"],
                "brand": "SimpleBrand",
                "warranty": "1 year"
            },
            review_count=50,
            average_rating=4.0
        )
        db.add(test_product)
        db.commit()
        db.refresh(test_product)
        print(f"   ✅ Test product created: {test_product.name} (ID: {test_product.id})")
        
        # Test 2: Test Q&A Content Type
        print("\n2. Testing Q&A Content Type...")
        print("   Testing create_ai_llm_optimized_content with content_type='qa'...")
        
        start_time = time.time()
        
        result = optimizer.create_ai_llm_optimized_content(
            "Simple Q&A Topic",
            "qa",  # Q&A content type
            str(test_product.id)
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"   Duration: {duration:.2f} seconds")
        
        if "error" not in result:
            print(f"   ✅ Q&A content creation successful!")
            print(f"      - Content ID: {result.get('content_id', 'N/A')}")
            print(f"      - Topic: {result.get('topic', 'N/A')}")
            print(f"      - Content type: {result.get('content_type', 'N/A')}")
            print(f"      - AI LLM optimized: {result.get('ai_llm_optimized', False)}")
            
            # Check content structure
            base_content = result.get('base_content', {})
            if base_content:
                print(f"      - Base content generated: ✅")
                qa_pairs = base_content.get('qa_pairs', [])
                print(f"        • Q&A pairs: {len(qa_pairs)} pairs")
            
            qa_content = result.get('qa_content', {})
            if qa_content:
                qa_pairs = qa_content.get('qa_pairs', [])
                print(f"      - Q&A content: {len(qa_pairs)} pairs")
            
            # Check if Q&A content is the same as base content (should be for qa type)
            if base_content == qa_content:
                print(f"      - ✅ Q&A content matches base content (correct)")
            else:
                print(f"      - ⚠️ Q&A content differs from base content")
            
        else:
            print(f"   ❌ Q&A content creation failed: {result.get('error')}")
            return False
        
        # Test 3: Test Blog Content Type (for comparison)
        print("\n3. Testing Blog Content Type (for comparison)...")
        print("   Testing create_ai_llm_optimized_content with content_type='blog'...")
        
        start_time = time.time()
        
        result2 = optimizer.create_ai_llm_optimized_content(
            "Simple Blog Topic",
            "blog",  # Blog content type
            str(test_product.id)
        )
        
        end_time = time.time()
        duration2 = end_time - start_time
        
        print(f"   Duration: {duration2:.2f} seconds")
        
        if "error" not in result2:
            print(f"   ✅ Blog content creation successful!")
            print(f"      - Content ID: {result2.get('content_id', 'N/A')}")
            print(f"      - Content type: {result2.get('content_type', 'N/A')}")
            
            # Check if Q&A content was generated separately
            qa_content2 = result2.get('qa_content', {})
            if qa_content2:
                qa_pairs2 = qa_content2.get('qa_pairs', [])
                print(f"      - Separate Q&A content: {len(qa_pairs2)} pairs")
        else:
            print(f"   ❌ Blog content creation failed: {result2.get('error')}")
        
        print(f"\n🎉 Simple AI LLM Optimizer Test Completed!")
        print(f"   Total test time: {time.time() - start_time:.2f} seconds")
        
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
        
        db.close()

if __name__ == "__main__":
    success = test_ai_llm_simple()
    if success:
        print("\n✅ All simple tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some simple tests failed!")
        sys.exit(1) 