import unittest
from unittest.mock import patch
from agents import sales_genie

class TestSalesGenieAdsIntegration(unittest.TestCase):
    @patch("services.pinterest_ads_api.create_pinterest_ad")
    @patch("services.pinterest_ads_api.get_pinterest_ad_metrics")
    @patch("services.meta_ads_api.create_meta_ad")
    @patch("services.meta_ads_api.get_meta_ad_metrics")
    @patch("services.shopify_api.create_product")
    @patch("services.cj_api.fetch_mock_products")
    def test_full_agent_ad_workflow(self, mock_fetch, mock_shopify, mock_meta_metrics, mock_meta_create, mock_pin_metrics, mock_pin_create):
        # Arrange
        mock_fetch.return_value = [{
            "name": "CoolPinProd",
            "cost": 12,
            "retail_price": 22,
            "shipping_time_days": 6,
            "rating": 4.3,
            "tags": ["pinterest", "meta"],
            "category": "general"
        }]
        mock_shopify.return_value = True
        mock_meta_create.return_value = {"status": "success", "ad_id": "meta_test_10"}
        mock_meta_metrics.return_value = (38, 120)
        mock_pin_create.return_value = {"status": "success", "ad_id": "pin_test_10"}
        mock_pin_metrics.return_value = (45, 100)

        # Act
        sales_genie.main()
        # Assert: Add assertions here as you expand your agent (logs, summaries, etc.)

if __name__ == "__main__":
    unittest.main()
