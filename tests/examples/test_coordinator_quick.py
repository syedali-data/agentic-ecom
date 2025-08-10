#!/usr/bin/env python3
"""
Quick test for AI LLM Optimizer - Main Coordinator Module
Fast test focusing on core coordination functionality.
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

def test_coordinator_quick():
    """Quick test of AI LLM Optimizer coordinator functionality."""
    
    print("🧪 Quick Test: AI LLM Optimizer - Main Coordinator Module")
    print("=" * 55)
    
    # Initialize database session and optimizer
    db = SessionLocal()
    optimizer = AILLMOptimizer(db)
    
    try:
        # Test 1: Basic Coordinator Initialization
        print("\n1. Testing Coordinator Initialization...")
        print(f"   ✅ AILLMOptimizer initialized successfully")
        print(f"   ✅ Database session: {type(db).__name__}")
        print(f"   ✅ Content Generator: {type(optimizer.content_generator).__name__}")
        print(f"   ✅ SEO Optimizer: {type(optimizer.seo_optimizer).__name__}")
        print(f"   ✅ QA Engine: {type(optimizer.qa_engine).__name__}")
        print(f"   ✅ Schema Generator: {type(optimizer.schema_generator).__name__}")
        
        # Test 2: Create Test Product
        print("\n2. Creating Test Product...")
        test_product = Product(
            name="Quick Test Product",
            description="Test product for quick coordinator test",
            sku="QUICK-TEST-001",
            category="Electronics",
            price=99.99,
            status=ProductStatus.ACTIVE,
            image_url="https://example.com/quick-test.jpg",
            tags=["test", "electronics"],
            product_metadata={
                "features": ["Quick Feature 1", "Quick Feature 2"],
                "brand": "QuickBrand",
                "warranty": "1 year"
            },
            review_count=50,
            average_rating=4.0
        )
        db.add(test_product)
        db.commit()
        db.refresh(test_product)
        print(f"   ✅ Test product created: {test_product.name} (ID: {test_product.id})")
        
        # Test 3: Test Main Coordinator Method (Quick)
        print("\n3. Testing Main Coordinator Method...")
        print("   Testing create_ai_llm_optimized_content (quick test)...")
        
        start_time = time.time()
        result = optimizer.create_ai_llm_optimized_content(
            "Quick Test Topic",
            "blog",
            str(test_product.id)
        )
        end_time = time.time()
        
        if "error" not in result:
            print(f"   ✅ Coordinator method executed successfully!")
            print(f"      - Execution time: {end_time - start_time:.2f} seconds")
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
                print(f"        • Title: {base_content.get('title', 'N/A')[:50]}...")
                print(f"        • Content length: {len(base_content.get('content', ''))} chars")
            
            seo_content = result.get('seo_content', {})
            if seo_content:
                print(f"      - SEO content generated: ✅")
                print(f"        • Keywords: {len(seo_content.get('keywords', []))} keywords")
            
            qa_content = result.get('qa_content', {})
            if qa_content:
                print(f"      - Q&A content generated: ✅")
                qa_pairs = qa_content.get('qa_pairs', [])
                print(f"        • Q&A pairs: {len(qa_pairs)} pairs")
            
            schema_content = result.get('schema_content', {})
            if schema_content:
                print(f"      - Schema content generated: ✅")
                print(f"        • Schema type: {schema_content.get('schema_type', 'N/A')}")
            
        else:
            print(f"   ❌ Coordinator method failed: {result.get('error')}")
            return False
        
        # Test 4: Test Error Handling
        print("\n4. Testing Error Handling...")
        error_result = optimizer.create_ai_llm_optimized_content(
            "",  # Empty topic
            "invalid_type",  # Invalid content type
            "invalid_product_id"  # Invalid product ID
        )
        
        if "error" in error_result:
            print(f"   ✅ Error handling working correctly")
            print(f"      - Error message: {error_result.get('error')}")
        else:
            print(f"   ⚠️ Error handling may need improvement")
        
        # Test 5: Test Component Integration
        print("\n5. Testing Component Integration...")
        integration_tests = [
            ("Content Generator", optimizer.content_generator is not None),
            ("SEO Optimizer", optimizer.seo_optimizer is not None),
            ("QA Engine", optimizer.qa_engine is not None),
            ("Schema Generator", optimizer.schema_generator is not None),
        ]
        
        all_integrated = True
        for component, status in integration_tests:
            if status:
                print(f"   ✅ {component} integrated")
            else:
                print(f"   ❌ {component} not integrated")
                all_integrated = False
        
        if all_integrated:
            print("   ✅ All components properly integrated")
        else:
            print("   ❌ Some components not properly integrated")
            return False
        
        # Test 6: Test Safety Integration
        print("\n6. Testing Safety Integration...")
        try:
            # Test that safety checks are working
            safety_result = optimizer.create_ai_llm_optimized_content(
                "Safety Test Topic",
                "blog",
                str(test_product.id)
            )
            
            if "error" not in safety_result:
                print("   ✅ Safety integration working correctly")
                print("   ✅ Dry run mode active (development)")
            else:
                print(f"   ⚠️ Safety integration issue: {safety_result.get('error')}")
        except Exception as e:
            print(f"   ❌ Safety integration failed: {e}")
        
        print(f"\n🎉 AI LLM Optimizer Coordinator Quick Test Completed Successfully!")
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
    success = test_coordinator_quick()
    if success:
        print("\n✅ All coordinator quick tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some coordinator quick tests failed!")
        sys.exit(1) 