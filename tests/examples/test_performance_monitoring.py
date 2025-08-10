#!/usr/bin/env python3
"""
Performance Monitoring and Feedback System Test
Demonstrates comprehensive performance monitoring, feedback collection, and insights.
"""

import sys
import os
import time
import threading
from datetime import datetime, timedelta

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database import Base
from db.models import Product, InventoryItem, ProductStatus, EventLog, EventType
from revenue_optimization.inventory_prediction_engine import InventoryPredictionEngine
from revenue_optimization.performance_monitor import LiveInventoryPerformanceMonitor, PerformanceAlert, SystemFeedback

def setup_database():
    """Set up test database."""
    try:
        # Create in-memory SQLite database for testing
        engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        Base.metadata.create_all(engine)
        
        # Create session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        
        return session
        
    except Exception as e:
        print(f"❌ Failed to setup database: {e}")
        return None

def create_test_products(session):
    """Create test products with inventory."""
    try:
        # Create test products
        products = [
            Product(
                name="Performance Test Product 1",
                description="A test product for performance monitoring",
                sku="PERF001",
                category="ELECTRONICS",
                price=99.99,
                status=ProductStatus.ACTIVE
            ),
            Product(
                name="Performance Test Product 2", 
                description="Another test product for monitoring",
                sku="PERF002",
                category="CLOTHING",
                price=49.99,
                status=ProductStatus.ACTIVE
            ),
            Product(
                name="Performance Test Product 3",
                description="Third test product for monitoring",
                sku="PERF003", 
                category="HOME_GARDEN",
                price=29.99,
                status=ProductStatus.ACTIVE
            )
        ]
        
        for product in products:
            session.add(product)
        
        session.commit()
        
        # Create inventory items
        inventory_items = [
            InventoryItem(
                product_id=products[0].id,
                quantity=100,
                reserved_quantity=10,
                available_quantity=90,
                low_stock_threshold=20
            ),
            InventoryItem(
                product_id=products[1].id,
                quantity=50,
                reserved_quantity=5,
                available_quantity=45,
                low_stock_threshold=15
            ),
            InventoryItem(
                product_id=products[2].id,
                quantity=25,
                reserved_quantity=0,
                available_quantity=25,
                low_stock_threshold=10
            )
        ]
        
        for item in inventory_items:
            session.add(item)
        
        session.commit()
        
        print(f"✅ Created {len(products)} test products with inventory")
        return products
        
    except Exception as e:
        print(f"❌ Failed to create test products: {e}")
        return []

def create_test_events(session):
    """Create test events for performance monitoring."""
    try:
        # Create various test events
        events = [
            EventLog(
                event_type=EventType.INVENTORY_UPDATED,
                source="performance_test",
                data={"product_id": "1", "old_quantity": 100, "new_quantity": 95},
                created_at=datetime.now() - timedelta(minutes=30)
            ),
            EventLog(
                event_type=EventType.INVENTORY_UPDATED,  # Use existing event type
                source="performance_test",
                data={"products_synced": 3, "changes_detected": 1},
                created_at=datetime.now() - timedelta(minutes=15)
            ),
            EventLog(
                event_type=EventType.PRODUCT_UPDATED,  # Use existing event type
                source="performance_test",
                data={"error": "Test error for monitoring"},
                created_at=datetime.now() - timedelta(minutes=5)
            ),
            EventLog(
                event_type=EventType.INVENTORY_UPDATED,
                source="performance_test",
                data={"product_id": "2", "old_quantity": 50, "new_quantity": 45},
                created_at=datetime.now() - timedelta(minutes=2)
            )
        ]
        
        for event in events:
            session.add(event)
        
        session.commit()
        print(f"✅ Created {len(events)} test events")
        
    except Exception as e:
        print(f"❌ Failed to create test events: {e}")

def alert_callback(alert: PerformanceAlert):
    """Callback function for performance alerts."""
    print(f"🚨 ALERT: {alert.alert_type.upper()} - {alert.severity.upper()}")
    print(f"   Message: {alert.message}")
    print(f"   Metrics: {alert.metrics}")
    print(f"   Timestamp: {alert.timestamp}")
    print("   " + "="*50)

def feedback_callback(feedback: SystemFeedback):
    """Callback function for feedback notifications."""
    print(f"📝 FEEDBACK: {feedback.feedback_type.upper()} - {feedback.rating}/5")
    print(f"   Comment: {feedback.comment}")
    print(f"   User ID: {feedback.user_id or 'Anonymous'}")
    print(f"   Timestamp: {feedback.timestamp}")
    print("   " + "="*50)

def test_performance_monitoring():
    """Test performance monitoring capabilities."""
    print("🚀 Testing Performance Monitoring System")
    print("=" * 60)
    
    # Setup database
    session = setup_database()
    if not session:
        return
    
    # Create test data
    products = create_test_products(session)
    if not products:
        return
    
    create_test_events(session)
    
    # Initialize inventory engine and performance monitor
    inventory_engine = InventoryPredictionEngine(session)
    performance_monitor = LiveInventoryPerformanceMonitor(session, inventory_engine)
    
    # Subscribe to alerts and feedback
    performance_monitor.subscribe_to_alerts(alert_callback)
    performance_monitor.subscribe_to_feedback(feedback_callback)
    
    print("\n📊 Starting Performance Monitoring...")
    print("-" * 40)
    
    # Start monitoring
    if performance_monitor.start_monitoring(interval_seconds=10):
        print("✅ Performance monitoring started")
        
        # Collect initial metrics
        print("\n📈 Collecting Initial Performance Metrics...")
        initial_metrics = performance_monitor.collect_performance_metrics()
        print(f"   CPU Usage: {initial_metrics.cpu_usage}%")
        print(f"   Memory Usage: {initial_metrics.memory_usage}%")
        print(f"   Response Time: {initial_metrics.response_time}s")
        print(f"   Error Rate: {initial_metrics.error_rate}%")
        print(f"   Inventory Changes: {initial_metrics.inventory_changes}")
        print(f"   Sync Operations: {initial_metrics.sync_operations}")
        print(f"   Prediction Accuracy: {initial_metrics.prediction_accuracy}%")
        
        # Simulate some activity
        print("\n🔄 Simulating System Activity...")
        print("-" * 30)
        
        # Simulate inventory changes
        for i, product in enumerate(products):
            print(f"   Simulating inventory change for {product.name}...")
            inventory = session.query(InventoryItem).filter(
                InventoryItem.product_id == product.id
            ).first()
            
            if inventory:
                old_quantity = inventory.quantity
                inventory.quantity -= 5
                inventory.available_quantity = inventory.quantity - inventory.reserved_quantity
                session.commit()
                print(f"     ✅ Changed: {old_quantity} -> {inventory.quantity}")
        
        # Add some feedback
        print("\n📝 Adding User Feedback...")
        print("-" * 25)
        
        feedback_samples = [
            ("performance", 4, "System response time is good", "user_123"),
            ("accuracy", 5, "Predictions are very accurate", "user_456"),
            ("usability", 3, "Interface could be more intuitive", "user_789"),
            ("reliability", 4, "System is stable and reliable", "user_101")
        ]
        
        for feedback_type, rating, comment, user_id in feedback_samples:
            result = performance_monitor.add_feedback(feedback_type, rating, comment, user_id)
            if "error" not in result:
                print(f"   ✅ Feedback added: {feedback_type} - {rating}/5")
            else:
                print(f"   ❌ Failed to add feedback: {result['error']}")
        
        # Wait for monitoring to collect more data
        print("\n⏳ Waiting for monitoring to collect data...")
        time.sleep(15)
        
        # Collect updated metrics
        print("\n📈 Collecting Updated Performance Metrics...")
        updated_metrics = performance_monitor.collect_performance_metrics()
        print(f"   CPU Usage: {updated_metrics.cpu_usage}%")
        print(f"   Memory Usage: {updated_metrics.memory_usage}%")
        print(f"   Response Time: {updated_metrics.response_time}s")
        print(f"   Error Rate: {updated_metrics.error_rate}%")
        print(f"   Inventory Changes: {updated_metrics.inventory_changes}")
        print(f"   Sync Operations: {updated_metrics.sync_operations}")
        print(f"   Prediction Accuracy: {updated_metrics.prediction_accuracy}%")
        
        # Generate performance report
        print("\n📊 Generating Performance Report...")
        print("-" * 35)
        
        report = performance_monitor.get_performance_report(hours=1)
        
        if "error" not in report:
            print(f"   Report Period: {report['report_period']}")
            print(f"   System Health: {report['system_health']}")
            
            # Performance statistics
            stats = report.get('performance_statistics', {})
            if stats:
                averages = stats.get('averages', {})
                print(f"\n   Performance Averages:")
                print(f"     CPU Usage: {averages.get('cpu_usage', 0)}%")
                print(f"     Memory Usage: {averages.get('memory_usage', 0)}%")
                print(f"     Response Time: {averages.get('response_time', 0)}s")
                print(f"     Error Rate: {averages.get('error_rate', 0)}%")
                print(f"     Prediction Accuracy: {averages.get('prediction_accuracy', 0)}%")
                
                totals = stats.get('totals', {})
                print(f"\n   Performance Totals:")
                print(f"     Inventory Changes: {totals.get('inventory_changes', 0)}")
                print(f"     Sync Operations: {totals.get('sync_operations', 0)}")
                print(f"     Throughput: {totals.get('throughput', 0)}")
                
                trends = stats.get('trends', {})
                print(f"\n   Performance Trends:")
                print(f"     CPU Usage: {trends.get('cpu_usage', 'stable')}")
                print(f"     Memory Usage: {trends.get('memory_usage', 'stable')}")
                print(f"     Response Time: {trends.get('response_time', 'stable')}")
            
            # Alerts
            alerts = report.get('alerts', [])
            print(f"\n   Alerts ({len(alerts)}):")
            for alert in alerts[:3]:  # Show first 3 alerts
                print(f"     • {alert['alert_type']}: {alert['message']} ({alert['severity']})")
            
            # Feedback summary
            feedback_summary = report.get('feedback_summary', {})
            print(f"\n   Feedback Summary:")
            print(f"     Total Feedback: {feedback_summary.get('total_feedback', 0)}")
            print(f"     Average Rating: {feedback_summary.get('average_rating', 0)}/5")
            
            averages_by_type = feedback_summary.get('averages_by_type', {})
            if averages_by_type:
                print(f"     Averages by Type:")
                for feedback_type, avg_rating in averages_by_type.items():
                    print(f"       {feedback_type}: {avg_rating}/5")
            
            # Recommendations
            recommendations = report.get('recommendations', [])
            print(f"\n   Recommendations:")
            for i, recommendation in enumerate(recommendations, 1):
                print(f"     {i}. {recommendation}")
        
        else:
            print(f"   ❌ Failed to generate report: {report['error']}")
        
        # Stop monitoring
        print("\n🛑 Stopping Performance Monitoring...")
        performance_monitor.stop_monitoring()
        print("✅ Performance monitoring stopped")
        
    else:
        print("❌ Failed to start performance monitoring")
    
    session.close()
    print("\n🎯 Performance Monitoring Test Completed!")

def test_feedback_system():
    """Test feedback collection and analysis."""
    print("\n📝 Testing Feedback System")
    print("=" * 40)
    
    # Setup database
    session = setup_database()
    if not session:
        return
    
    # Initialize components
    inventory_engine = InventoryPredictionEngine(session)
    performance_monitor = LiveInventoryPerformanceMonitor(session, inventory_engine)
    
    # Test feedback collection
    print("\n📊 Testing Feedback Collection...")
    print("-" * 30)
    
    feedback_data = [
        ("performance", 5, "Excellent system performance!", "user_001"),
        ("accuracy", 4, "Very accurate predictions", "user_002"),
        ("usability", 3, "Good but could be better", "user_003"),
        ("reliability", 5, "Rock solid system", "user_004"),
        ("performance", 2, "Sometimes slow", "user_005"),
        ("accuracy", 4, "Predictions are good", "user_006"),
        ("usability", 4, "Easy to use", "user_007"),
        ("reliability", 3, "Occasional issues", "user_008")
    ]
    
    for feedback_type, rating, comment, user_id in feedback_data:
        result = performance_monitor.add_feedback(feedback_type, rating, comment, user_id)
        if "error" not in result:
            print(f"   ✅ {feedback_type}: {rating}/5 - {comment[:30]}...")
        else:
            print(f"   ❌ Failed: {result['error']}")
    
    # Test feedback analysis
    print("\n📈 Testing Feedback Analysis...")
    print("-" * 30)
    
    feedback_summary = performance_monitor._get_feedback_summary(hours=1)
    
    print(f"   Total Feedback: {feedback_summary.get('total_feedback', 0)}")
    print(f"   Average Rating: {feedback_summary.get('average_rating', 0)}/5")
    
    averages_by_type = feedback_summary.get('averages_by_type', {})
    if averages_by_type:
        print(f"   Averages by Type:")
        for feedback_type, avg_rating in averages_by_type.items():
            print(f"     {feedback_type}: {avg_rating}/5")
    
    feedback_distribution = feedback_summary.get('feedback_distribution', {})
    if feedback_distribution:
        print(f"   Rating Distribution:")
        for rating, count in feedback_distribution.items():
            if count > 0:
                print(f"     {rating.replace('_', ' ').title()}: {count}")
    
    session.close()
    print("\n✅ Feedback System Test Completed!")

def test_alert_system():
    """Test alert generation and notification."""
    print("\n🚨 Testing Alert System")
    print("=" * 35)
    
    # Setup database
    session = setup_database()
    if not session:
        return
    
    # Initialize components
    inventory_engine = InventoryPredictionEngine(session)
    performance_monitor = LiveInventoryPerformanceMonitor(session, inventory_engine)
    
    # Subscribe to alerts
    performance_monitor.subscribe_to_alerts(alert_callback)
    
    print("\n📊 Testing Alert Generation...")
    print("-" * 30)
    
    # Test different alert scenarios
    test_metrics = [
        # High CPU usage
        type('MockMetrics', (), {
            'cpu_usage': 85.0,
            'memory_usage': 60.0,
            'response_time': 2.0,
            'error_rate': 1.0,
            'inventory_changes': 5,
            'sync_operations': 2,
            'prediction_accuracy': 85.0
        })(),
        
        # High memory usage
        type('MockMetrics', (), {
            'cpu_usage': 50.0,
            'memory_usage': 90.0,
            'response_time': 1.5,
            'error_rate': 0.5,
            'inventory_changes': 3,
            'sync_operations': 1,
            'prediction_accuracy': 88.0
        })(),
        
        # Slow response time
        type('MockMetrics', (), {
            'cpu_usage': 30.0,
            'memory_usage': 45.0,
            'response_time': 7.0,
            'error_rate': 2.0,
            'inventory_changes': 2,
            'sync_operations': 1,
            'prediction_accuracy': 82.0
        })(),
        
        # High error rate
        type('MockMetrics', (), {
            'cpu_usage': 40.0,
            'memory_usage': 55.0,
            'response_time': 2.5,
            'error_rate': 8.0,
            'inventory_changes': 4,
            'sync_operations': 2,
            'prediction_accuracy': 75.0
        })()
    ]
    
    for i, metrics in enumerate(test_metrics, 1):
        print(f"   Testing Alert Scenario {i}...")
        alerts = performance_monitor._check_for_alerts(metrics)
        
        if alerts:
            for alert in alerts:
                print(f"     🚨 Generated: {alert.alert_type} - {alert.severity}")
        else:
            print(f"     ✅ No alerts generated")
    
    # Test alert retrieval
    print("\n📋 Testing Alert Retrieval...")
    print("-" * 30)
    
    recent_alerts = performance_monitor._get_recent_alerts(hours=1)
    print(f"   Recent Alerts: {len(recent_alerts)}")
    
    for alert in recent_alerts[:3]:  # Show first 3 alerts
        print(f"     • {alert['alert_type']}: {alert['message']} ({alert['severity']})")
    
    session.close()
    print("\n✅ Alert System Test Completed!")

if __name__ == "__main__":
    print("🎯 Performance Monitoring and Feedback System Test")
    print("=" * 60)
    
    try:
        # Test 1: Performance monitoring
        test_performance_monitoring()
        
        # Test 2: Feedback system
        test_feedback_system()
        
        # Test 3: Alert system
        test_alert_system()
        
        print("\n🎉 All performance monitoring tests completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc() 