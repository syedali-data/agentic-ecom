#!/usr/bin/env python3
"""
Live Inventory Tracking Test Script
Demonstrates the new live inventory tracking and synchronization capabilities.
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
from db.models import Base, Product, InventoryItem, ProductStatus
from revenue_optimization.inventory_prediction_engine import InventoryPredictionEngine, LiveInventoryUpdate

def setup_database():
    """Set up test database."""
    try:
        # Create in-memory SQLite database for testing
        engine = create_engine("sqlite:///:memory:")
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
                name="Test Product 1",
                description="A test product for inventory tracking",
                sku="TEST001",
                category="ELECTRONICS",
                price=99.99,
                status=ProductStatus.ACTIVE
            ),
            Product(
                name="Test Product 2", 
                description="Another test product",
                sku="TEST002",
                category="CLOTHING",
                price=49.99,
                status=ProductStatus.ACTIVE
            ),
            Product(
                name="Test Product 3",
                description="Third test product",
                sku="TEST003", 
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

def inventory_update_callback(update: LiveInventoryUpdate):
    """Callback function for inventory updates."""
    print(f"🔄 INVENTORY UPDATE: {update.product_id}")
    print(f"   Old Quantity: {update.old_quantity}")
    print(f"   New Quantity: {update.new_quantity}")
    print(f"   Change Type: {update.change_type}")
    print(f"   Source: {update.source}")
    print(f"   Timestamp: {update.timestamp}")
    print(f"   Change Amount: {update.metadata.get('change_amount', 0)}")
    print(f"   Percentage Change: {update.metadata.get('percentage_change', 0):.1f}%")
    print("   " + "="*50)

def test_live_inventory_tracking():
    """Test live inventory tracking capabilities."""
    print("🚀 Testing Live Inventory Tracking Capabilities")
    print("=" * 60)
    
    # Setup database
    session = setup_database()
    if not session:
        return
    
    # Create test products
    products = create_test_products(session)
    if not products:
        return
    
    # Initialize inventory prediction engine
    engine = InventoryPredictionEngine(session)
    
    print("\n📊 Initial Inventory Status:")
    print("-" * 30)
    
    # Get initial live status
    initial_status = engine.get_live_inventory_status()
    if "error" not in initial_status:
        print(f"Total Products: {initial_status['total_products']}")
        print(f"Active Products: {initial_status['active_products']}")
        print(f"Out of Stock: {initial_status['out_of_stock_products']}")
        print(f"Low Stock: {initial_status['low_stock_products']}")
        print(f"High Risk: {initial_status['high_risk_products']}")
    
    print("\n🔔 Subscribing to Inventory Updates...")
    engine.subscribe_to_inventory_updates(inventory_update_callback)
    
    print("\n🔄 Enabling Live Tracking...")
    if engine.enable_live_tracking(interval_seconds=5):  # Check every 5 seconds for demo
        print("✅ Live tracking enabled successfully")
        
        # Simulate inventory changes
        print("\n📦 Simulating Inventory Changes...")
        print("-" * 30)
        
        # Change 1: Restock
        print("1. Simulating restock for Product 1...")
        inventory1 = session.query(InventoryItem).filter(
            InventoryItem.product_id == products[0].id
        ).first()
        if inventory1:
            old_quantity = inventory1.quantity
            inventory1.quantity += 50
            inventory1.available_quantity = inventory1.quantity - inventory1.reserved_quantity
            session.commit()
            print(f"   ✅ Restocked: {old_quantity} -> {inventory1.quantity}")
        
        time.sleep(6)  # Wait for tracking to detect change
        
        # Change 2: Order (decrease)
        print("\n2. Simulating order for Product 2...")
        inventory2 = session.query(InventoryItem).filter(
            InventoryItem.product_id == products[1].id
        ).first()
        if inventory2:
            old_quantity = inventory2.quantity
            inventory2.quantity -= 20
            inventory2.available_quantity = inventory2.quantity - inventory2.reserved_quantity
            session.commit()
            print(f"   ✅ Order processed: {old_quantity} -> {inventory2.quantity}")
        
        time.sleep(6)  # Wait for tracking to detect change
        
        # Change 3: Adjustment
        print("\n3. Simulating inventory adjustment for Product 3...")
        inventory3 = session.query(InventoryItem).filter(
            InventoryItem.product_id == products[2].id
        ).first()
        if inventory3:
            old_quantity = inventory3.quantity
            inventory3.quantity = 30  # Direct adjustment
            inventory3.available_quantity = inventory3.quantity - inventory3.reserved_quantity
            session.commit()
            print(f"   ✅ Adjustment: {old_quantity} -> {inventory3.quantity}")
        
        time.sleep(6)  # Wait for tracking to detect change
        
        print("\n📊 Final Live Inventory Status:")
        print("-" * 30)
        
        # Get final live status
        final_status = engine.get_live_inventory_status()
        if "error" not in final_status:
            print(f"Total Products: {final_status['total_products']}")
            print(f"Active Products: {final_status['active_products']}")
            print(f"Out of Stock: {final_status['out_of_stock_products']}")
            print(f"Low Stock: {final_status['low_stock_products']}")
            print(f"High Risk: {final_status['high_risk_products']}")
            
            if final_status['summary']:
                print(f"\nSummary:")
                print(f"  Average Days of Inventory: {final_status['summary']['average_days_of_inventory']:.1f}")
                print(f"  Average Stockout Risk: {final_status['summary']['average_stockout_risk']:.2f}")
                print(f"  Total Available Stock: {final_status['summary']['total_available_stock']}")
        
        # Test individual product status
        print(f"\n🔍 Individual Product Status:")
        print("-" * 30)
        for product in products:
            status = engine.get_live_inventory_status(product.id)
            if "error" not in status:
                print(f"Product: {product.name}")
                print(f"  Current Stock: {status['current_stock']}")
                print(f"  Available Stock: {status['available_stock']}")
                print(f"  Stockout Risk: {status['stockout_risk']}")
                print(f"  Days of Inventory: {status['days_of_inventory']}")
                print(f"  Status: {status['status']}")
                print()
        
        # Test inventory sync
        print("🔄 Testing Inventory Sync with External Systems...")
        print("-" * 40)
        sync_results = engine.sync_inventory_with_external_systems(force_sync=True)
        if "error" not in sync_results:
            print(f"Products Synced: {sync_results['products_synced']}")
            print(f"Changes Detected: {sync_results['changes_detected']}")
            print(f"Errors: {len(sync_results['errors'])}")
            
            if sync_results['details']:
                print("\nSync Details:")
                for detail in sync_results['details'][:3]:  # Show first 3
                    print(f"  Product {detail['product_id']}: {'✅' if detail['synced'] else '❌'}")
                    if detail.get('changes_detected'):
                        print(f"    Changes: {detail['old_quantity']} -> {detail['new_quantity']}")
        
        print("\n🛑 Disabling Live Tracking...")
        engine.disable_live_tracking()
        print("✅ Live tracking disabled")
        
    else:
        print("❌ Failed to enable live tracking")
    
    session.close()
    print("\n🎯 Live Inventory Tracking Test Completed!")

def test_inventory_prediction_with_live_tracking():
    """Test inventory prediction with live tracking enabled."""
    print("\n🔮 Testing Inventory Prediction with Live Tracking")
    print("=" * 50)
    
    # Setup database
    session = setup_database()
    if not session:
        return
    
    # Create test products
    products = create_test_products(session)
    if not products:
        return
    
    # Initialize engine
    engine = InventoryPredictionEngine(session)
    
    # Enable live tracking
    engine.enable_live_tracking(interval_seconds=10)
    
    print("\n📊 Predicting Inventory Needs (with live tracking)...")
    
    # Test single product prediction
    if products:
        prediction = engine.predict_inventory_needs(
            product_id=products[0].id,
            days=30,
            include_recommendations=True
        )
        
        if "error" not in prediction:
            print(f"\nProduct: {prediction['product_name']}")
            print(f"Current Stock: {prediction['current_stock']}")
            print(f"Predicted Demand: {prediction['predicted_demand']}")
            print(f"Recommended Order: {prediction['recommended_order']}")
            print(f"Stockout Risk: {prediction['stockout_risk']}")
            print(f"Days of Inventory: {prediction['days_of_inventory']}")
            
            if prediction.get('recommendations'):
                print(f"\nRecommendations:")
                for action in prediction['recommendations'].get('immediate_actions', []):
                    print(f"  • {action}")
    
    # Test all products prediction
    print("\n📈 Predicting All Products...")
    all_predictions = engine.predict_inventory_needs(days=30, include_recommendations=True)
    
    if "error" not in all_predictions:
        print(f"Total Products: {all_predictions['total_products']}")
        print(f"High Risk Products: {all_predictions['high_risk_products']}")
        print(f"Low Stock Products: {all_predictions['low_stock_products']}")
        
        if all_predictions.get('summary'):
            summary = all_predictions['summary']
            print(f"\nSummary:")
            print(f"  Average Days of Inventory: {summary['average_days_of_inventory']:.1f}")
            print(f"  Total Recommended Order: {summary['total_recommended_order']}")
    
    # Disable tracking
    engine.disable_live_tracking()
    session.close()
    
    print("\n✅ Inventory Prediction with Live Tracking Test Completed!")

if __name__ == "__main__":
    print("🎯 Live Inventory Tracking System Test")
    print("=" * 50)
    
    try:
        # Test 1: Live inventory tracking
        test_live_inventory_tracking()
        
        # Test 2: Inventory prediction with live tracking
        test_inventory_prediction_with_live_tracking()
        
        print("\n🎉 All tests completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc() 