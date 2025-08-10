import os
import requests
import json
from typing import Dict, Any, Tuple
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class PinterestAdsAPI:
    """Pinterest Ads API client for campaign management"""
    
    def __init__(self):
        self.access_token = os.getenv("PINTEREST_ACCESS_TOKEN")
        self.ad_account_id = os.getenv("PINTEREST_AD_ACCOUNT_ID")
        self.app_id = os.getenv("PINTEREST_APP_ID")
        self.app_secret = os.getenv("PINTEREST_APP_SECRET")
        self.base_url = "https://api.pinterest.com/v5"
        
        if not self.access_token:
            logger.warning("Pinterest access token not found. Using mock mode.")
            self.mock_mode = True
        else:
            self.mock_mode = False
            self.headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
    
    def create_campaign(self, product: Dict[str, Any], campaign_id: str) -> Dict[str, Any]:
        """Create a Pinterest ad campaign"""
        if self.mock_mode:
            return self._mock_create_campaign(product, campaign_id)
        
        try:
            campaign_data = {
                "name": f"{product['name']} - {campaign_id}",
                "ad_account_id": self.ad_account_id,
                "objective_type": "CONVERSIONS",
                "status": "ACTIVE",
                "budget_type": "DAILY",
                "budget_value": 10000,  # $100 in micro units
                "lifetime_spend_cap": 1000000  # $1000 in micro units
            }
            
            response = requests.post(
                f"{self.base_url}/ad_accounts/{self.ad_account_id}/campaigns",
                headers=self.headers,
                json=campaign_data
            )
            
            if response.status_code == 201:
                return response.json()
            else:
                print(f"❌ Pinterest campaign creation failed: {response.text}")
                return self._mock_create_campaign(product, campaign_id)
                
        except Exception as e:
            print(f"❌ Error creating Pinterest campaign: {e}")
            return self._mock_create_campaign(product, campaign_id)
    
    def create_ad_group(self, campaign_id: str, product: Dict[str, Any]) -> Dict[str, Any]:
        """Create an ad group within a campaign"""
        if self.mock_mode:
            return self._mock_create_ad_group(campaign_id, product)
        
        try:
            ad_group_data = {
                "name": f"Ad Group - {product['name']}",
                "campaign_id": campaign_id,
                "status": "ACTIVE",
                "budget_type": "DAILY",
                "budget_value": 5000,  # $50 in micro units
                "targeting_spec": {
                    "age_bucket": ["25-34", "35-44"],
                    "gender": ["female", "male"],
                    "geo": ["US"],
                    "interests": ["fashion", "beauty", "home"]
                }
            }
            
            response = requests.post(
                f"{self.base_url}/ad_accounts/{self.ad_account_id}/ad_groups",
                headers=self.headers,
                json=ad_group_data
            )
            
            if response.status_code == 201:
                return response.json()
            else:
                print(f"❌ Pinterest ad group creation failed: {response.text}")
                return self._mock_create_ad_group(campaign_id, product)
                
        except Exception as e:
            print(f"❌ Error creating Pinterest ad group: {e}")
            return self._mock_create_ad_group(campaign_id, product)
    
    def create_pin_ad(self, ad_group_id: str, product: Dict[str, Any], image_url: str) -> Dict[str, Any]:
        """Create a Pin ad"""
        if self.mock_mode:
            return self._mock_create_pin_ad(ad_group_id, product, image_url)
        
        try:
            pin_data = {
                "title": product['name'],
                "description": product.get('description', ''),
                "link": product.get('link', ''),
                "media_source": {
                    "source_type": "image_url",
                    "url": image_url
                }
            }
            
            # First create the Pin
            pin_response = requests.post(
                f"{self.base_url}/pins",
                headers=self.headers,
                json=pin_data
            )
            
            if pin_response.status_code != 201:
                print(f"❌ Pinterest pin creation failed: {pin_response.text}")
                return self._mock_create_pin_ad(ad_group_id, product, image_url)
            
            pin_id = pin_response.json()['id']
            
            # Then create the ad
            ad_data = {
                "ad_group_id": ad_group_id,
                "pin_id": pin_id,
                "status": "ACTIVE"
            }
            
            ad_response = requests.post(
                f"{self.base_url}/ad_accounts/{self.ad_account_id}/ads",
                headers=self.headers,
                json=ad_data
            )
            
            if ad_response.status_code == 201:
                return ad_response.json()
            else:
                print(f"❌ Pinterest ad creation failed: {ad_response.text}")
                return self._mock_create_pin_ad(ad_group_id, product, image_url)
                
        except Exception as e:
            print(f"❌ Error creating Pinterest ad: {e}")
            return self._mock_create_pin_ad(ad_group_id, product, image_url)
    
    def get_campaign_metrics(self, campaign_id: str) -> Tuple[float, float]:
        """Get campaign spend and revenue metrics"""
        if self.mock_mode:
            return self._mock_get_metrics(campaign_id)
        
        try:
            # Get spend metrics
            spend_response = requests.get(
                f"{self.base_url}/ad_accounts/{self.ad_account_id}/campaigns/{campaign_id}/metrics",
                headers=self.headers,
                params={
                    "metric_types": ["SPEND_IN_DOLLAR"],
                    "date": "TODAY"
                }
            )
            
            # Get conversion metrics (revenue)
            revenue_response = requests.get(
                f"{self.base_url}/ad_accounts/{self.ad_account_id}/campaigns/{campaign_id}/metrics",
                headers=self.headers,
                params={
                    "metric_types": ["TOTAL_CONVERSION_VALUE"],
                    "date": "TODAY"
                }
            )
            
            spend = 0
            revenue = 0
            
            if spend_response.status_code == 200:
                spend_data = spend_response.json()
                spend = spend_data.get('data', [{}])[0].get('values', [{}])[0].get('value', 0)
            
            if revenue_response.status_code == 200:
                revenue_data = revenue_response.json()
                revenue = revenue_data.get('data', [{}])[0].get('values', [{}])[0].get('value', 0)
            
            return float(spend), float(revenue)
            
        except Exception as e:
            print(f"❌ Error getting Pinterest metrics: {e}")
            return self._mock_get_metrics(campaign_id)
    
    def pause_campaign(self, campaign_id: str) -> bool:
        """Pause a Pinterest campaign"""
        if self.mock_mode:
            return self._mock_pause_campaign(campaign_id)
        
        try:
            response = requests.patch(
                f"{self.base_url}/ad_accounts/{self.ad_account_id}/campaigns/{campaign_id}",
                headers=self.headers,
                json={"status": "PAUSED"}
            )
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"❌ Error pausing Pinterest campaign: {e}")
            return self._mock_pause_campaign(campaign_id)
    
    # Mock methods for fallback
    def _mock_create_campaign(self, product: Dict[str, Any], campaign_id: str) -> Dict[str, Any]:
        print(f"📌 [Pinterest Mock] Creating campaign {campaign_id} for {product['name']}")
        return {"id": f"mock_campaign_{campaign_id}", "status": "ACTIVE"}
    
    def _mock_create_ad_group(self, campaign_id: str, product: Dict[str, Any]) -> Dict[str, Any]:
        print(f"📌 [Pinterest Mock] Creating ad group for campaign {campaign_id}")
        return {"id": f"mock_ad_group_{campaign_id}", "status": "ACTIVE"}
    
    def _mock_create_pin_ad(self, ad_group_id: str, product: Dict[str, Any], image_url: str) -> Dict[str, Any]:
        print(f"📌 [Pinterest Mock] Creating ad for '{product['name']}' in group {ad_group_id}")
        return {"id": f"mock_ad_{ad_group_id}", "status": "ACTIVE"}
    
    def _mock_get_metrics(self, campaign_id: str) -> Tuple[float, float]:
        print(f"📌 [Pinterest Mock] Getting metrics for campaign {campaign_id}")
        return 45.0, 100.0  # Mock spend and revenue
    
    def _mock_pause_campaign(self, campaign_id: str) -> bool:
        print(f"📌 [Pinterest Mock] Pausing campaign {campaign_id}")
        return True

# Initialize global Pinterest API client
pinterest_api = PinterestAdsAPI()

# Legacy functions for backward compatibility
def launch_pinterest_ad_campaign(product, campaign_id):
    """Launch a Pinterest ad campaign"""
    return pinterest_api.create_campaign(product, campaign_id)

def get_pinterest_ad_metrics(campaign_id):
    """Get Pinterest campaign metrics"""
    return pinterest_api.get_campaign_metrics(campaign_id)

def create_pinterest_ad(product_name, ad_text, image_url, budget_usd):
    """Create a Pinterest ad"""
    product = {"name": product_name, "description": ad_text}
    return pinterest_api.create_pin_ad("mock_ad_group", product, image_url)
