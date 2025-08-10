#!/usr/bin/env python3
"""
Safety Test Script for Agentic-Ecom
Tests all safety measures before running any real operations.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.safety_manager import safety_manager
from agents.sales_genie import is_kill_switch_on

def test_safety_system():
    """Test the safety system"""
    print("🔒 Testing Safety System")
    print("=" * 50)
    
    # Test 1: Kill switch
    print("\n1. Testing Kill Switch:")
    kill_switch_active = is_kill_switch_on()
    print(f"   Kill switch active: {kill_switch_active}")
    if kill_switch_active:
        print("   ✅ Kill switch is working (system is paused)")
    else:
        print("   ⚠️ Kill switch is not active")
    
    # Test 2: Environment configuration
    print("\n2. Testing Environment Configuration:")
    status = safety_manager.get_safety_status()
    print(f"   Environment: {status['environment']}")
    print(f"   Max budget: ${status['max_budget']}")
    print(f"   Dry run mode: {status['dry_run_mode']}")
    print(f"   Requires approval: {status['requires_approval']}")
    
    # Test 3: Safety checks
    print("\n3. Testing Safety Checks:")
    
    # Test campaign creation
    campaign_check = safety_manager.check_environment_safety("create_campaign", "meta_ads")
    print(f"   Campaign creation: {'✅ SAFE' if campaign_check['safe'] else '❌ BLOCKED'}")
    if campaign_check['reason']:
        print(f"   Reason: {campaign_check['reason']}")
    
    # Test spend tracking
    spend_check = safety_manager.check_environment_safety("spend_$50", "meta_ads")
    print(f"   Spend $50: {'✅ SAFE' if spend_check['safe'] else '❌ BLOCKED'}")
    if spend_check['reason']:
        print(f"   Reason: {spend_check['reason']}")
    
    # Test 4: Budget tracking
    print("\n4. Testing Budget Tracking:")
    print(f"   Current daily spend: ${status['daily_spend']}")
    print(f"   Budget remaining: ${status['budget_remaining']}")
    
    # Test 5: Simulate actions
    print("\n5. Testing Action Simulation:")
    
    # Simulate campaign creation
    print("   Simulating campaign creation...")
    success = safety_manager.track_campaign_creation("meta_ads")
    print(f"   Campaign creation: {'✅ SUCCESS' if success else '❌ BLOCKED'}")
    
    # Simulate spend
    print("   Simulating $10 spend...")
    success = safety_manager.track_spend(10.0, "meta_ads")
    print(f"   Spend tracking: {'✅ SUCCESS' if success else '❌ BLOCKED'}")
    
    # Test 6: Final status
    print("\n6. Final Safety Status:")
    final_status = safety_manager.get_safety_status()
    print(f"   Daily spend: ${final_status['daily_spend']}")
    print(f"   Campaign count: {final_status['campaign_count']}")
    print(f"   Budget remaining: ${final_status['budget_remaining']}")
    
    return True

def test_api_safety():
    """Test API safety measures"""
    print("\n🔌 Testing API Safety")
    print("=" * 50)
    
    # Test Meta Ads API
    print("\n1. Testing Meta Ads API:")
    try:
        from services.meta_ads_api import meta_api
        print(f"   Meta API mock mode: {meta_api.mock_mode}")
        print(f"   Meta API access token: {'✅ Present' if meta_api.access_token else '❌ Missing'}")
    except Exception as e:
        print(f"   ❌ Meta API error: {e}")
    
    # Test Pinterest API
    print("\n2. Testing Pinterest API:")
    try:
        from services.pinterest_ads_api import pinterest_api
        print(f"   Pinterest API mock mode: {pinterest_api.mock_mode}")
        print(f"   Pinterest API access token: {'✅ Present' if pinterest_api.access_token else '❌ Missing'}")
    except Exception as e:
        print(f"   ❌ Pinterest API error: {e}")
    
    # Test Shopify API
    print("\n3. Testing Shopify API:")
    try:
        from services.shopify_api import get_products
        print("   ✅ Shopify API functions available")
    except Exception as e:
        print(f"   ❌ Shopify API error: {e}")

def main():
    """Main test function"""
    print("🚀 Agentic-Ecom Safety Test")
    print("=" * 60)
    
    try:
        # Test safety system
        test_safety_system()
        
        # Test API safety
        test_api_safety()
        
        print("\n" + "=" * 60)
        print("✅ Safety tests completed successfully!")
        print("\n📋 Recommendations:")
        print("1. Keep kill switch active during development")
        print("2. Use dry run mode for testing")
        print("3. Set low budget limits for development")
        print("4. Always test with mock APIs first")
        
    except Exception as e:
        print(f"\n❌ Safety test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 