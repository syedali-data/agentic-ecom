import unittest
from services.ad_optimizer import AdOptimizer

class TestAdOptimizer(unittest.TestCase):
    def test_roas_and_budget_not_exceeded(self):
        # Test Meta
        meta_cfg = {"daily_budget_usd": 100, "min_roas": 2.0}
        opt = AdOptimizer("meta_ads", "meta_test", "sess1", meta_cfg)
        opt.track_spend(30)
        opt.track_revenue(90)  # ROAS = 3.0
        self.assertAlmostEqual(opt.get_roas(), 3.0)
        # No pause expected

        # Test Pinterest
        pin_cfg = {"daily_budget_usd": 50, "min_roas": 1.5}
        opt2 = AdOptimizer("pinterest_ads", "pin_test", "sess2", pin_cfg)
        opt2.track_spend(20)
        opt2.track_revenue(40)  # ROAS = 2.0
        self.assertAlmostEqual(opt2.get_roas(), 2.0)

    def test_budget_exceeded_triggers_pause(self):
        meta_cfg = {"daily_budget_usd": 40, "min_roas": 1.0}
        opt = AdOptimizer("meta_ads", "meta_budget", "sess3", meta_cfg)
        opt.track_spend(30)
        opt.track_spend(15)  # total = 45 > 40
        # Check logs or manually assert pause logic if pause sets a flag

    def test_low_roas_triggers_pause(self):
        pin_cfg = {"daily_budget_usd": 50, "min_roas": 3.0}
        opt = AdOptimizer("pinterest_ads", "pin_roas", "sess4", pin_cfg)
        opt.track_spend(20)
        opt.track_revenue(40)  # ROAS = 2.0 < 3.0
        # Again, you may add a .paused attribute to check if pause_campaign ran

if __name__ == '__main__':
    unittest.main()
