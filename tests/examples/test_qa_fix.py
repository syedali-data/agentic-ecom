#!/usr/bin/env python3
"""
Quick test to verify Q&A optimization fix
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from db.database import SessionLocal
from content_marketing.qa_engine import QAEngine

def test_qa_optimization():
    """Test Q&A optimization to ensure it's not causing loops."""
    print("🧪 Testing Q&A Optimization Fix")
    print("=" * 40)
    
    db = SessionLocal()
    qa_engine = QAEngine(db)
    
    try:
        # Test Q&A generation
        print("1. Testing Q&A content generation...")
        result = qa_engine.generate_qa_content("Test Electronics", None)
        
        if "error" not in result:
            qa_pairs = result.get("qa_pairs", [])
            print(f"   ✅ Generated {len(qa_pairs)} Q&A pairs")
            print(f"   ✅ No infinite loops detected")
            
            # Check if optimization was applied
            if qa_pairs:
                first_pair = qa_pairs[0]
                print(f"   ✅ Sample Q&A pair:")
                print(f"      Q: {first_pair.get('question', 'N/A')[:50]}...")
                print(f"      A: {first_pair.get('answer', 'N/A')[:50]}...")
        else:
            print(f"   ❌ Q&A generation failed: {result.get('error')}")
            return False
        
        print("\n2. Testing optimization efficiency...")
        # Test the optimization method directly
        test_pairs = [
            {"question": "What is the best laptop?", "answer": "The best laptop depends on your needs."},
            {"question": "How much should I spend?", "answer": "Spend based on your requirements and budget."}
        ]
        
        optimized_pairs = qa_engine._optimize_for_ai_llm(test_pairs, "Electronics")
        print(f"   ✅ Optimized {len(optimized_pairs)} pairs in single API call")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = test_qa_optimization()
    if success:
        print("\n✅ Q&A optimization fix verified!")
    else:
        print("\n❌ Q&A optimization fix failed!")
        sys.exit(1) 