#!/usr/bin/env python3
"""
Simple test to verify that all content marketing modules can be imported correctly.
"""

import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all modules can be imported"""
    try:
        print("Testing imports...")
        
        # Test content marketing modules
        from content_marketing.generator import ContentGenerator
        print("✅ ContentGenerator imported successfully")
        
        from content_marketing.seo_optimizer import SEOOptimizer
        print("✅ SEOOptimizer imported successfully")
        
        from content_marketing.qa_engine import QAEngine
        print("✅ QAEngine imported successfully")
        
        from content_marketing.schema_markup import SchemaMarkupGenerator
        print("✅ SchemaMarkupGenerator imported successfully")
        
        from content_marketing.performance_tracker import ContentPerformanceTracker
        print("✅ ContentPerformanceTracker imported successfully")
        
        from content_marketing.ai_llm_optimizer import AILLMOptimizer
        print("✅ AILLMOptimizer imported successfully")
        
        # Test that classes can be instantiated with mock objects
        from unittest.mock import Mock
        
        mock_db = Mock()
        
        # Test ContentGenerator
        generator = ContentGenerator(mock_db)
        print("✅ ContentGenerator instantiated successfully")
        
        # Test SEOOptimizer
        seo_optimizer = SEOOptimizer(mock_db)
        print("✅ SEOOptimizer instantiated successfully")
        
        # Test QAEngine
        qa_engine = QAEngine(mock_db)
        print("✅ QAEngine instantiated successfully")
        
        # Test SchemaMarkupGenerator
        schema_generator = SchemaMarkupGenerator(mock_db)
        print("✅ SchemaMarkupGenerator instantiated successfully")
        
        # Test ContentPerformanceTracker
        performance_tracker = ContentPerformanceTracker(mock_db)
        print("✅ ContentPerformanceTracker instantiated successfully")
        
        # Test AILLMOptimizer
        ai_llm_optimizer = AILLMOptimizer(mock_db)
        print("✅ AILLMOptimizer instantiated successfully")
        
        print("\n🎉 All imports and instantiations successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1) 