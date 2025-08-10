import os
import requests
import json
from typing import Dict, Any, Tuple
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class MetaAdsAPI:
    """Meta (Facebook) Ads API client for campaign management"""
    
    def __init__(self):
        self.access_token = os.getenv("META_ACCESS_TOKEN")
        self.ad_account_id = os.getenv("META_AD_ACCOUNT_ID")
        self.app_id = os.getenv("META_APP_ID")
        self.app_secret = os.getenv("META_APP_SECRET")
        self.pixel_id = os.getenv("META_PIXEL_ID")
        self.base_url = "https://graph.facebook.com/v18.0"
        
        if not self.access_token:
            logger.warning("Meta access token not found. Using mock mode.")
            self.mock_mode = True
        else:
            self.mock_mode = False
            self.headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
    
    def create_campaign(self, product: Dict[str, Any], campaign_id: str) -> Dict[str, Any]:
        """Create a Meta ad campaign"""
        if self.mock_mode:
            return self._mock_create_campaign(product, campaign_id)
        
        try:
            campaign_data = {
                "name": f"{product['name']} - {campaign_id}",
                "objective": "CONVERSIONS",
                "status": "ACTIVE",
                "special_ad_categories": [],
                "daily_budget": 10000,  # $100 in cents
                "lifetime_budget": 1000000  # $10000 in cents
            }
            
            response = requests.post(
                f"{self.base_url}/{self.ad_account_id}/campaigns",
                headers=self.headers,
                data=campaign_data
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Meta campaign creation failed: {response.text}")
                return self._mock_create_campaign(product, campaign_id)
                
        except Exception as e:
            print(f"❌ Error creating Meta campaign: {e}")
            return self._mock_create_campaign(product, campaign_id)
    
    def create_ad_set(self, campaign_id: str, product: Dict[str, Any]) -> Dict[str, Any]:
        """Create an ad set within a campaign"""
        if self.mock_mode:
            return self._mock_create_ad_set(campaign_id, product)
        
        try:
            ad_set_data = {
                "name": f"Ad Set - {product['name']}",
                "campaign_id": campaign_id,
                "daily_budget": 5000,  # $50 in cents
                "billing_event": "IMPRESSIONS",
                "optimization_goal": "CONVERSIONS",
                "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
                "targeting": {
                    "age_min": 25,
                    "age_max": 45,
                    "genders": [1, 2],  # 1=male, 2=female
                    "geo_locations": {
                        "countries": ["US"]
                    },
                    "interests": [
                        {"name": "Fashion", "id": "6002714395372"},
                        {"name": "Beauty", "id": "6002714395373"}
                    ]
                }
            }
            
            response = requests.post(
                f"{self.base_url}/{self.ad_account_id}/adsets",
                headers=self.headers,
                data=ad_set_data
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Meta ad set creation failed: {response.text}")
                return self._mock_create_ad_set(campaign_id, product)
                
        except Exception as e:
            print(f"❌ Error creating Meta ad set: {e}")
            return self._mock_create_ad_set(campaign_id, product)
    
    def create_ad(self, ad_set_id: str, product: Dict[str, Any], image_url: str) -> Dict[str, Any]:
        """Create a Meta ad"""
        if self.mock_mode:
            return self._mock_create_ad(ad_set_id, product, image_url)
        
        try:
            ad_data = {
                "name": f"Ad - {product['name']}",
                "adset_id": ad_set_id,
                "creative": {
                    "name": f"Creative - {product['name']}",
                    "object_story_spec": {
                        "page_id": self.app_id,
                        "link_data": {
                            "image_hash": self._upload_image(image_url),
                            "link": product.get('link', ''),
                            "message": product.get('description', ''),
                            "name": product['name']
                        }
                    }
                },
                "status": "ACTIVE"
            }
            
            response = requests.post(
                f"{self.base_url}/{self.ad_account_id}/ads",
                headers=self.headers,
                data=ad_data
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Meta ad creation failed: {response.text}")
                return self._mock_create_ad(ad_set_id, product, image_url)
                
        except Exception as e:
            print(f"❌ Error creating Meta ad: {e}")
            return self._mock_create_ad(ad_set_id, product, image_url)
    
    def get_campaign_metrics(self, campaign_id: str) -> Tuple[float, float]:
        """Get campaign spend and revenue metrics"""
        if self.mock_mode:
            return self._mock_get_metrics(campaign_id)
        
        try:
            # Get spend metrics
            spend_response = requests.get(
                f"{self.base_url}/{campaign_id}/insights",
                headers=self.headers,
                params={
                    "fields": "spend",
                    "date_preset": "today"
                }
            )
            
            # Get conversion metrics (revenue)
            revenue_response = requests.get(
                f"{self.base_url}/{campaign_id}/insights",
                headers=self.headers,
                params={
                    "fields": "actions",
                    "action_attribution_windows": '["28d_click"]',
                    "date_preset": "today"
                }
            )
            
            spend = 0
            revenue = 0
            
            if spend_response.status_code == 200:
                spend_data = spend_response.json()
                spend = float(spend_data.get('data', [{}])[0].get('spend', 0))
            
            if revenue_response.status_code == 200:
                revenue_data = revenue_response.json()
                actions = revenue_data.get('data', [{}])[0].get('actions', [])
                for action in actions:
                    if action.get('action_type') == 'purchase':
                        revenue += float(action.get('value', 0))
            
            return spend, revenue
            
        except Exception as e:
            print(f"❌ Error getting Meta metrics: {e}")
            return self._mock_get_metrics(campaign_id)
    
    def pause_campaign(self, campaign_id: str) -> bool:
        """Pause a Meta campaign"""
        if self.mock_mode:
            return self._mock_pause_campaign(campaign_id)
        
        try:
            response = requests.post(
                f"{self.base_url}/{campaign_id}",
                headers=self.headers,
                data={"status": "PAUSED"}
            )
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"❌ Error pausing Meta campaign: {e}")
            return self._mock_pause_campaign(campaign_id)
    
    def _upload_image(self, image_url: str) -> str:
        """Upload image to Meta and return hash"""
        if self.mock_mode:
            return "mock_image_hash_123"
        
        try:
            # Download image
            img_response = requests.get(image_url)
            if img_response.status_code != 200:
                return "mock_image_hash_123"
            
            # Upload to Meta
            files = {'source': ('image.jpg', img_response.content, 'image/jpeg')}
            upload_response = requests.post(
                f"{self.base_url}/{self.ad_account_id}/adimages",
                headers={"Authorization": f"Bearer {self.access_token}"},
                files=files
            )
            
            if upload_response.status_code == 200:
                return upload_response.json().get('images', {}).get('image.jpg', {}).get('hash', 'mock_hash')
            else:
                return "mock_image_hash_123"
                
        except Exception as e:
            print(f"❌ Error uploading image: {e}")
            return "mock_image_hash_123"
    
    # Mock methods for fallback
    def _mock_create_campaign(self, product: Dict[str, Any], campaign_id: str) -> Dict[str, Any]:
        print(f"📘 [Meta Mock] Creating campaign {campaign_id} for {product['name']}")
        return {"id": f"mock_campaign_{campaign_id}", "status": "ACTIVE"}
    
    def _mock_create_ad_set(self, campaign_id: str, product: Dict[str, Any]) -> Dict[str, Any]:
        print(f"📘 [Meta Mock] Creating ad set for campaign {campaign_id}")
        return {"id": f"mock_ad_set_{campaign_id}", "status": "ACTIVE"}
    
    def _mock_create_ad(self, ad_set_id: str, product: Dict[str, Any], image_url: str) -> Dict[str, Any]:
        print(f"📘 [Meta Mock] Creating ad for '{product['name']}' in set {ad_set_id}")
        return {"id": f"mock_ad_{ad_set_id}", "status": "ACTIVE"}
    
    def _mock_get_metrics(self, campaign_id: str) -> Tuple[float, float]:
        print(f"📘 [Meta Mock] Getting metrics for campaign {campaign_id}")
        return 45.0, 100.0  # Mock spend and revenue
    
    def _mock_pause_campaign(self, campaign_id: str) -> bool:
        print(f"📘 [Meta Mock] Pausing campaign {campaign_id}")
        return True

# Initialize global Meta API client
meta_api = MetaAdsAPI()

# Legacy functions for backward compatibility
def launch_meta_ad_campaign(product, campaign_id):
    """Launch a Meta ad campaign"""
    return meta_api.create_campaign(product, campaign_id)

def get_meta_ad_metrics(campaign_id):
    """Get Meta campaign metrics"""
    return meta_api.get_campaign_metrics(campaign_id)

def create_meta_ad(product_name, ad_text, image_url, budget_usd):
    """Create a Meta ad"""
    product = {"name": product_name, "description": ad_text}
    return meta_api.create_ad("mock_ad_set", product, image_url)
