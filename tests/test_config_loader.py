import unittest
from utils.config_loader import get_campaign_budget_config

class TestConfigLoader(unittest.TestCase):
    def setUp(self):
        self.config = {
            "meta_ads": {
                "default": {"daily_budget_usd": 200, "min_roas": 2.5},
                "campaigns": {
                    "meta1": {"daily_budget_usd": 100, "min_roas": 3.0}
                }
            },
            "pinterest_ads": {
                "default": {"daily_budget_usd": 50, "min_roas": 1.5}
            }
        }

    def test_default_and_override(self):
        # Gets override if exists
        cfg = get_campaign_budget_config("meta_ads", "meta1", self.config)
        self.assertEqual(cfg["daily_budget_usd"], 100)
        # Gets default if not in campaigns
        cfg2 = get_campaign_budget_config("meta_ads", "meta_notfound", self.config)
        self.assertEqual(cfg2["daily_budget_usd"], 200)
        # Gets correct for Pinterest default
        cfg3 = get_campaign_budget_config("pinterest_ads", "anything", self.config)
        self.assertEqual(cfg3["daily_budget_usd"], 50)

if __name__ == '__main__':
    unittest.main()
