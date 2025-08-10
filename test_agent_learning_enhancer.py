#!/usr/bin/env python3
"""
Test Script for Agent Learning Enhancer
Demonstrates how to use the AgentLearningEnhancer to improve agent intelligence.
"""

import sys
import os
import json
from datetime import datetime

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_agent_learning_enhancer():
    """Test the AgentLearningEnhancer functionality."""
    print("🧠 Testing Agent Learning Enhancer")
    print("=" * 50)
    
    try:
        # Import required modules
        from agents.agent_learning_enhancer import AgentLearningEnhancer
        from db.database import get_db
        
        # Get database session
        db = get_db()
        
        # Initialize the enhancer
        enhancer = AgentLearningEnhancer(db)
        print("✅ AgentLearningEnhancer initialized")
        
        # Test with different agent types
        agents = ["sales_genie", "logibot", "buybot"]
        
        for agent_type in agents:
            print(f"\n🔍 Testing {agent_type}...")
            
            # 1. Enrich training data
            print("📊 Enriching training data...")
            enriched_data = enhancer.enrich_agent_training_data(agent_type)
            
            if "error" in enriched_data:
                print(f"❌ Error enriching data: {enriched_data['error']}")
                continue
            
            print(f"✅ Enriched {agent_type}")
            print(f"   📈 Data sources: {enriched_data['data_sources']}")
            print(f"   🔍 Insights: {len(enriched_data['insights'])}")
            print(f"   💡 Recommendations: {enriched_data['recommendations']}")
            
            # 2. Create training dataset
            print("📊 Creating training dataset...")
            dataset = enhancer.create_agent_training_dataset(agent_type, days=30)
            
            if "error" in dataset:
                print(f"❌ Error creating dataset: {dataset['error']}")
                continue
            
            print(f"✅ Dataset created for {agent_type}")
            print(f"   📈 Training examples: {len(dataset['training_examples'])}")
            print(f"   🎯 Optimization targets: {dataset['optimization_targets']}")
            
            # 3. Optimize prompts
            print("🎯 Optimizing prompts...")
            optimized_prompts = enhancer.optimize_agent_prompts(agent_type)
            
            if "error" in optimized_prompts:
                print(f"❌ Error optimizing prompts: {optimized_prompts['error']}")
                continue
            
            print(f"✅ Prompts optimized for {agent_type}")
            print(f"   📊 Optimization goal: {optimized_prompts['optimization_goal']}")
            
            # 4. Display performance metrics
            if dataset.get('performance_metrics'):
                metrics = dataset['performance_metrics']
                print(f"   📊 Performance metrics:")
                print(f"      Views: {metrics.get('total_views', 0):,}")
                print(f"      Engagement: {metrics.get('overall_engagement_rate', 0):.2%}")
                print(f"      Conversion: {metrics.get('conversion_rate', 0):.2%}")
        
        print(f"\n🎉 Agent Learning Enhancer test completed!")
        print("=" * 50)
        
        # Demonstrate advanced usage
        print("\n🚀 Advanced Usage Examples:")
        
        # Example 1: Weekly review
        print("\n1. Weekly Agent Review:")
        weekly_review(enhancer)
        
        # Example 2: Performance monitoring
        print("\n2. Performance Monitoring:")
        performance_monitoring(enhancer)
        
        # Example 3: Automated optimization
        print("\n3. Automated Optimization:")
        automated_optimization(enhancer)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all required modules are available.")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def weekly_review(enhancer):
    """Demonstrate weekly agent review."""
    try:
        agents = ["sales_genie", "logibot", "buybot"]
        
        for agent_type in agents:
            print(f"   🔍 Reviewing {agent_type}...")
            
            # Enrich training data
            enriched = enhancer.enrich_agent_training_data(agent_type)
            print(f"      📊 {len(enriched.get('insights', []))} insights found")
            
            # Create training dataset
            dataset = enhancer.create_agent_training_dataset(agent_type, days=7)
            print(f"      📈 {len(dataset.get('training_examples', []))} training examples")
            
            # Optimize prompts
            optimized = enhancer.optimize_agent_prompts(agent_type)
            print(f"      🎯 Prompts optimized for {optimized.get('optimization_goal', 'performance')}")
            
            # Print recommendations
            recommendations = enriched.get('recommendations', [])
            for rec in recommendations:
                print(f"      💡 Recommendation: {rec}")
    
    except Exception as e:
        print(f"   ❌ Error in weekly review: {e}")

def performance_monitoring(enhancer):
    """Demonstrate performance monitoring."""
    try:
        agents = ["sales_genie", "logibot", "buybot"]
        
        for agent_type in agents:
            print(f"   📊 Monitoring {agent_type}...")
            
            dataset = enhancer.create_agent_training_dataset(agent_type, days=30)
            metrics = dataset.get('performance_metrics', {})
            
            print(f"      Views: {metrics.get('total_views', 0):,}")
            print(f"      Engagement: {metrics.get('overall_engagement_rate', 0):.2%}")
            print(f"      Conversion: {metrics.get('conversion_rate', 0):.2%}")
            
            # Check for issues
            if metrics.get('overall_engagement_rate', 0) < 0.05:
                print(f"      ⚠️  Low engagement detected")
            
            if metrics.get('conversion_rate', 0) < 0.02:
                print(f"      ⚠️  Low conversion rate detected")
    
    except Exception as e:
        print(f"   ❌ Error in performance monitoring: {e}")

def automated_optimization(enhancer):
    """Demonstrate automated optimization."""
    try:
        agents = ["sales_genie", "logibot", "buybot"]
        
        for agent_type in agents:
            print(f"   🤖 Optimizing {agent_type}...")
            
            dataset = enhancer.create_agent_training_dataset(agent_type, days=7)
            targets = dataset.get('optimization_targets', [])
            
            if targets:
                print(f"      🎯 Optimization targets: {targets}")
                
                optimized = enhancer.optimize_agent_prompts(agent_type, "performance")
                print(f"      ✅ Prompts optimized")
            else:
                print(f"      ✅ No optimization needed")
    
    except Exception as e:
        print(f"   ❌ Error in automated optimization: {e}")

if __name__ == "__main__":
    test_agent_learning_enhancer() 