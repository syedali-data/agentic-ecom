import unittest
from unittest.mock import patch
from services import pinterest_ads_api

class TestPinterestAdsAPI(unittest.TestCase):
    @patch("services.pinterest_ads_api.create_pinterest_ad")
    def test_create_pinterest_ad(self, mock_create):
        mock_create.return_value = {"status": "success", "ad_id": "pin_Test_77"}
        product_name = "TestProduct"
        ad_text = "Pin now!"
        image_url = "http://example.com/pin.png"
        budget_usd = 77

        result = pinterest_ads_api.create_pinterest_ad(product_name, ad_text, image_url, budget_usd)

        self.assertEqual(result["status"], "success")
        self.assertTrue(result["ad_id"].startswith("pin_"))
        mock_create.assert_called_once_with(product_name, ad_text, image_url, budget_usd)

    @patch("services.pinterest_ads_api.get_pinterest_ad_metrics")
    def test_get_pinterest_ad_metrics(self, mock_metrics):
        mock_metrics.return_value = (45.0, 100.0)
        campaign_id = "pin_abc_77"
        spend, revenue = pinterest_ads_api.get_pinterest_ad_metrics(campaign_id)
        self.assertEqual(spend, 45.0)
        self.assertEqual(revenue, 100.0)
        mock_metrics.assert_called_once_with(campaign_id)

if __name__ == "__main__":
    unittest.main()
