#!/usr/bin/env python3
"""
Test script for API authentication
"""

import requests
import json
import sys

# API base URL
BASE_URL = "http://127.0.0.1:8003"

def test_authentication():
    """Test the authentication system"""
    print("🔐 Testing API Authentication")
    print("=" * 50)
    
    # Test 1: Public endpoints (no auth required)
    print("\n1. Testing public endpoints...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Public endpoint accessible")
        else:
            print(f"❌ Public endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Public endpoint error: {e}")
    
    # Test 2: Protected endpoints (auth required)
    print("\n2. Testing protected endpoints (should fail without auth)...")
    try:
        response = requests.get(f"{BASE_URL}/products")
        if response.status_code == 401:
            print("✅ Protected endpoint correctly requires authentication")
        else:
            print(f"❌ Protected endpoint should require auth: {response.status_code}")
    except Exception as e:
        print(f"❌ Protected endpoint error: {e}")
    
    # Test 3: Login
    print("\n3. Testing login...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            print("✅ Login successful")
            print(f"   Token: {token_data['access_token'][:20]}...")
            print(f"   Role: {token_data['user_role']}")
            print(f"   Expires in: {token_data['expires_in']} seconds")
            
            # Test 4: Use token to access protected endpoints
            print("\n4. Testing protected endpoints with token...")
            headers = {
                "Authorization": f"Bearer {token_data['access_token']}"
            }
            
            # Test products endpoint
            response = requests.get(f"{BASE_URL}/products", headers=headers)
            if response.status_code == 200:
                print("✅ Products endpoint accessible with token")
            else:
                print(f"❌ Products endpoint failed: {response.status_code}")
            
            # Test analytics endpoint
            response = requests.get(f"{BASE_URL}/analytics/performance", headers=headers)
            if response.status_code == 200:
                print("✅ Analytics endpoint accessible with token")
            else:
                print(f"❌ Analytics endpoint failed: {response.status_code}")
            
            # Test 5: Test different user roles
            print("\n5. Testing different user roles...")
            
            # Test analyst login
            analyst_login = {
                "username": "analyst",
                "password": "analyst123"
            }
            
            response = requests.post(f"{BASE_URL}/auth/login", json=analyst_login)
            if response.status_code == 200:
                analyst_token = response.json()["access_token"]
                analyst_headers = {"Authorization": f"Bearer {analyst_token}"}
                
                # Analyst should be able to access analytics
                response = requests.get(f"{BASE_URL}/analytics/performance", headers=analyst_headers)
                if response.status_code == 200:
                    print("✅ Analyst can access analytics")
                else:
                    print(f"❌ Analyst cannot access analytics: {response.status_code}")
                
                # Analyst should not be able to access admin-only endpoints
                response = requests.get(f"{BASE_URL}/auth/users", headers=analyst_headers)
                if response.status_code == 403:
                    print("✅ Analyst correctly blocked from admin endpoint")
                else:
                    print(f"❌ Analyst should be blocked from admin endpoint: {response.status_code}")
            
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Login error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Authentication test completed!")

if __name__ == "__main__":
    test_authentication()
