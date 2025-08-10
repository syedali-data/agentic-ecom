#!/usr/bin/env python3
"""
Enhanced HITL Workflow System Demo

This script demonstrates the enhanced Human-in-the-Loop workflow system
with AI context and intelligent routing capabilities.
"""

import sys
import os
import logging
from datetime import datetime
from typing import List, Dict, Any

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.hitl_workflow import EnhancedHITLWorkflow
from schemas.hitl_queue import (
    HITLTaskType, HITLTaskPriority, HITLTaskStatus,
    AIContext, HITLWorkflowConfig
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def demo_enhanced_hitl_workflow():
    """Demonstrate the enhanced HITL workflow system."""
    
    print("🎯 Enhanced HITL Workflow System Demo")
    print("=" * 60)
    
    # Initialize workflow system
    workflow_system = EnhancedHITLWorkflow()
    
    print("\n📊 SYSTEM OVERVIEW")
    print("-" * 40)
    print("The Enhanced HITL Workflow System provides:")
    print("• AI-powered context and recommendations")
    print("• Intelligent workflow routing")
    print("• Automated escalation")
    print("• Performance tracking")
    print("• Compliance monitoring")
    
    # Demo 1: Create Product Review Task
    print(f"\n🔍 DEMO 1: Product Review Task with AI Context")
    print("-" * 50)
    
    product_task = workflow_system.create_task_with_ai_context(
        task_type=HITLTaskType.PRODUCT_REVIEW,
        title="Smart Fitness Tracker Review",
        description="Review the new Smart Fitness Tracker for approval",
        data={
            "product": {
                "name": "Smart Fitness Tracker Pro",
                "category": "electronics",
                "price": 89.99,
                "features": ["Heart rate monitoring", "GPS tracking", "Sleep analysis"]
            }
        },
        priority=HITLTaskPriority.HIGH,
        created_by="sales_genie",
        session_id="demo_session_001"
    )
    
    print(f"✅ Task Created: {product_task.id}")
    print(f"   Title: {product_task.title}")
    print(f"   Status: {product_task.status}")
    print(f"   Workflow Stage: {product_task.workflow_stage}")
    print(f"   Priority: {product_task.priority}")
    
    # Display AI context
    if product_task.ai_context:
        print(f"\n🤖 AI Context Generated:")
        print(f"   Analysis Summary: {product_task.ai_context.analysis_summary}")
        print(f"   Confidence Score: {product_task.ai_context.confidence_score:.3f}")
        print(f"   AI Model Used: {product_task.ai_context.ai_model_used}")
        print(f"   Risk Level: {product_task.ai_context.risk_assessment.get('overall_risk_level', 'unknown')}")
        
        if product_task.ai_context.recommendations:
            print(f"   Recommendations ({len(product_task.ai_context.recommendations)}):")
            for i, rec in enumerate(product_task.ai_context.recommendations[:3], 1):
                print(f"     {i}. {rec}")
    
    # Demo 2: Create Ad Approval Task
    print(f"\n📢 DEMO 2: Ad Approval Task with AI Context")
    print("-" * 50)
    
    ad_task = workflow_system.create_task_with_ai_context(
        task_type=HITLTaskType.AD_APPROVAL,
        title="Fitness Tracker Facebook Ad Review",
        description="Review Facebook ad for Smart Fitness Tracker",
        data={
            "ad": {
                "type": "facebook",
                "content": "Transform your fitness journey with our Smart Fitness Tracker Pro! Track heart rate, GPS, and sleep patterns. Limited time offer - 20% off!",
                "targeting": ["fitness enthusiasts", "health conscious", "25-45 age group"],
                "budget": 500
            }
        },
        priority=HITLTaskPriority.MEDIUM,
        created_by="sales_genie",
        session_id="demo_session_001"
    )
    
    print(f"✅ Task Created: {ad_task.id}")
    print(f"   Title: {ad_task.title}")
    print(f"   Status: {ad_task.status}")
    print(f"   Workflow Stage: {ad_task.workflow_stage}")
    
    # Display AI context
    if ad_task.ai_context:
        print(f"\n🤖 AI Context Generated:")
        print(f"   Analysis Summary: {ad_task.ai_context.analysis_summary}")
        print(f"   Confidence Score: {ad_task.ai_context.confidence_score:.3f}")
        print(f"   AI Model Used: {ad_task.ai_context.ai_model_used}")
        
        if ad_task.ai_context.suggested_actions:
            print(f"   Suggested Actions ({len(ad_task.ai_context.suggested_actions)}):")
            for i, action in enumerate(ad_task.ai_context.suggested_actions[:3], 1):
                print(f"     {i}. {action}")
    
    # Demo 3: Create Compliance Review Task
    print(f"\n⚖️ DEMO 3: Compliance Review Task with AI Context")
    print("-" * 50)
    
    compliance_task = workflow_system.create_task_with_ai_context(
        task_type=HITLTaskType.COMPLIANCE_REVIEW,
        title="Fitness Tracker Compliance Review",
        description="Review compliance requirements for Smart Fitness Tracker",
        data={
            "compliance": {
                "type": "product_safety",
                "regulations": ["FCC", "FDA", "CE"],
                "certifications_required": ["FCC ID", "FDA clearance", "CE marking"],
                "risk_factors": ["medical device classification", "data privacy"]
            }
        },
        priority=HITLTaskPriority.HIGH,
        created_by="compliance_officer",
        session_id="demo_session_001"
    )
    
    print(f"✅ Task Created: {compliance_task.id}")
    print(f"   Title: {compliance_task.title}")
    print(f"   Status: {compliance_task.status}")
    print(f"   Workflow Stage: {compliance_task.workflow_stage}")
    
    # Display AI context
    if compliance_task.ai_context:
        print(f"\n🤖 AI Context Generated:")
        print(f"   Analysis Summary: {compliance_task.ai_context.analysis_summary}")
        print(f"   Confidence Score: {compliance_task.ai_context.confidence_score:.3f}")
        print(f"   AI Model Used: {compliance_task.ai_context.ai_model_used}")
        
        if compliance_task.ai_context.compliance_check:
            compliance = compliance_task.ai_context.compliance_check
            print(f"   Compliance Status: {compliance.get('status', 'unknown')}")
            print(f"   Compliance Score: {compliance.get('compliance_score', 0):.3f}")
    
    # Demo 4: Process Task Actions
    print(f"\n🔄 DEMO 4: Processing Task Actions")
    print("-" * 50)
    
    # Process product task
    print(f"\n📊 Processing Product Review Task:")
    print(f"   Task ID: {product_task.id}")
    print(f"   Current Status: {product_task.status}")
    
    # Simulate human review and approval
    updated_product_task = workflow_system.process_task(
        task=product_task,
        action="approve",
        user_id="reviewer_001",
        notes="Product meets all requirements. AI analysis confirms high viral potential. Approved for launch."
    )
    
    print(f"   Action: approve")
    print(f"   New Status: {updated_product_task.status}")
    print(f"   Workflow Stage: {updated_product_task.workflow_stage}")
    print(f"   Completed At: {updated_product_task.completed_at}")
    
    # Process ad task with escalation
    print(f"\n📊 Processing Ad Approval Task:")
    print(f"   Task ID: {ad_task.id}")
    print(f"   Current Status: {ad_task.status}")
    
    # Simulate escalation
    updated_ad_task = workflow_system.process_task(
        task=ad_task,
        action="escalate",
        user_id="reviewer_001",
        notes="Ad content requires legal review due to health claims. Escalating to compliance team."
    )
    
    print(f"   Action: escalate")
    print(f"   New Status: {updated_ad_task.status}")
    print(f"   Workflow Stage: {updated_ad_task.workflow_stage}")
    print(f"   Escalation Reason: {updated_ad_task.escalation_reason}")
    
    # Demo 5: Workflow Analytics
    print(f"\n📈 DEMO 5: Workflow Analytics")
    print("-" * 50)
    
    analytics = workflow_system.get_workflow_analytics(days=30)
    
    print(f"📊 Workflow Performance (30 days):")
    print(f"   Total Tasks: {analytics['total_tasks']}")
    print(f"   Completed Tasks: {analytics['completed_tasks']}")
    print(f"   Pending Tasks: {analytics['pending_tasks']}")
    print(f"   Escalated Tasks: {analytics['escalated_tasks']}")
    print(f"   Average Completion Time: {analytics['average_completion_time_hours']:.1f} hours")
    print(f"   AI Accuracy Rate: {analytics['ai_accuracy_rate']:.1%}")
    print(f"   Auto-Approval Rate: {analytics['auto_approval_rate']:.1%}")
    print(f"   Escalation Rate: {analytics['escalation_rate']:.1%}")
    
    print(f"\n📊 Task Type Distribution:")
    for task_type, count in analytics['task_type_distribution'].items():
        print(f"   {task_type.replace('_', ' ').title()}: {count}")
    
    print(f"\n📊 Performance Trends:")
    for trend, direction in analytics['performance_trends'].items():
        print(f"   {trend.replace('_', ' ').title()}: {direction}")
    
    # Demo 6: Get Tasks for Review
    print(f"\n👥 DEMO 6: Tasks for Review")
    print("-" * 50)
    
    tasks_for_review = workflow_system.get_tasks_for_review(
        user_id="reviewer_001",
        task_type=HITLTaskType.PRODUCT_REVIEW
    )
    
    print(f"📋 Tasks Available for Review:")
    for i, task in enumerate(tasks_for_review, 1):
        print(f"   {i}. {task.title} ({task.task_type})")
        print(f"      Status: {task.status}")
        print(f"      Priority: {task.priority}")
        print(f"      Workflow Stage: {task.workflow_stage}")
        if task.ai_context:
            print(f"      AI Confidence: {task.ai_context.confidence_score:.3f}")
        print()
    
    # Demo 7: Workflow Configurations
    print(f"\n⚙️ DEMO 7: Workflow Configurations")
    print("-" * 50)
    
    configs = workflow_system.workflow_configs
    
    for task_type, config in configs.items():
        print(f"\n📋 {config.workflow_name}:")
        print(f"   Description: {config.description}")
        print(f"   Stages: {len(config.stages)}")
        print(f"   SLA: {config.sla_hours} hours")
        print(f"   Auto-Escalation: {'Enabled' if config.auto_escalation_enabled else 'Disabled'}")
        print(f"   AI Context: {'Enabled' if config.ai_context_enabled else 'Disabled'}")
        
        print(f"   Stages:")
        for stage in config.stages:
            print(f"     • {stage.stage_name}: {stage.description}")
            print(f"       - AI Analysis Required: {stage.ai_analysis_required}")
            print(f"       - Human Review Required: {stage.human_review_required}")
            print(f"       - Estimated Duration: {stage.estimated_duration_minutes} minutes")
    
    # Summary
    print(f"\n🎉 DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("✅ Enhanced HITL Workflow System Features Demonstrated:")
    print("   • AI-powered context generation")
    print("   • Intelligent workflow routing")
    print("   • Task creation and processing")
    print("   • Automated escalation")
    print("   • Performance analytics")
    print("   • Workflow configurations")
    print("   • Human review interface")
    
    print(f"\n🚀 Key Benefits:")
    print("   • Reduced manual review time")
    print("   • Improved decision accuracy")
    print("   • Automated risk assessment")
    print("   • Intelligent task routing")
    print("   • Comprehensive audit trail")
    print("   • Performance monitoring")
    
    return True

def demo_ai_context_generation():
    """Demonstrate AI context generation for different task types."""
    
    print(f"\n🤖 AI Context Generation Demo")
    print("=" * 50)
    
    workflow_system = EnhancedHITLWorkflow()
    
    # Test different task types
    task_types = [
        (HITLTaskType.TREND_ANALYSIS, "Trend Analysis for Electronics", {"trend": {"category": "electronics"}}),
        (HITLTaskType.CONTENT_REVIEW, "Blog Post Review", {"content": {"type": "blog", "text": "Sample blog content about fitness trackers"}}),
        (HITLTaskType.PERFORMANCE_OPTIMIZATION, "Ad Performance Optimization", {"performance": {"type": "ad_optimization"}})
    ]
    
    for task_type, title, data in task_types:
        print(f"\n📊 {title}:")
        print(f"   Task Type: {task_type}")
        
        task = workflow_system.create_task_with_ai_context(
            task_type=task_type,
            title=title,
            description=f"AI-enhanced {task_type} task",
            data=data,
            priority=HITLTaskPriority.MEDIUM
        )
        
        if task.ai_context:
            print(f"   AI Analysis: {task.ai_context.analysis_summary}")
            print(f"   Confidence Score: {task.ai_context.confidence_score:.3f}")
            print(f"   AI Model: {task.ai_context.ai_model_used}")
            print(f"   Risk Level: {task.ai_context.risk_assessment.get('overall_risk_level', 'unknown')}")
            
            if task.ai_context.recommendations:
                print(f"   Top Recommendation: {task.ai_context.recommendations[0] if task.ai_context.recommendations else 'None'}")
    
    print(f"\n✅ AI Context Generation Demo Completed!")

def main():
    """Run the complete enhanced HITL workflow demonstration."""
    
    print("🚀 Enhanced HITL Workflow System - Complete Demo")
    print("=" * 80)
    
    try:
        # Run main demo
        success1 = demo_enhanced_hitl_workflow()
        
        if success1:
            # Run AI context demo
            demo_ai_context_generation()
            
            print(f"\n{'='*80}")
            print("🎉 ALL DEMOS COMPLETED SUCCESSFULLY!")
            print("The Enhanced HITL Workflow System is fully operational.")
            print("Key features demonstrated:")
            print("  • AI-powered context and recommendations")
            print("  • Intelligent workflow routing")
            print("  • Automated escalation and approval")
            print("  • Performance tracking and analytics")
            print("  • Compliance monitoring")
            print("  • Human review interface")
            print(f"{'='*80}")
            
            return True
        else:
            print(f"\n❌ Demo failed. Please check the errors above.")
            return False
            
    except Exception as e:
        print(f"\n❌ Demo failed with exception: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 