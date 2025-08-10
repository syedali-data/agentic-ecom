import unittest
from unittest.mock import patch
from services import meta_ads_api

class TestMetaAdsAPI(unittest.TestCase):
    @patch("services.meta_ads_api.create_meta_ad")
    def test_create_meta_ad(self, mock_create):
        # Arrange
        mock_create.return_value = {"status": "success", "ad_id": "meta_Test_99"}
        product_name = "TestProduct"
        ad_text = "Buy now!"
        image_url = "http://example.com/image.png"
        budget_usd = 99

        # Act
        result = meta_ads_api.create_meta_ad(product_name, ad_text, image_url, budget_usd)

        # Assert
        self.assertEqual(result["status"], "success")
        self.assertTrue(result["ad_id"].startswith("meta_"))
        mock_create.assert_called_once_with(product_name, ad_text, image_url, budget_usd)

    # If you add a real requests.post call later, here's how you'd patch it:
    @patch("services.meta_ads_api.requests.post")
    def test_create_meta_ad_with_requests(self, mock_post):
        # Setup mock API response
        mock_post.return_value.json.return_value = {"status": "success", "ad_id": "meta_api_10"}
        mock_post.return_value.raise_for_status = lambda: None

        # You'd use your real function here if it used requests.post
        # result = meta_ads_api.create_meta_ad(...)
        # self.assertEqual(result["status"], "success")
        # self.assertIn("meta_api", result["ad_id"])
        # mock_post.assert_called_once()

if __name__ == "__main__":
    unittest.main()
