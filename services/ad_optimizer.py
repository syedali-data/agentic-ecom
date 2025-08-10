import logging
import os
import datetime
from decimal import Decimal
from utils.log_rotation import get_rotating_file_handler
from services.budget_guard import check_budget_limit

class AdOptimizer:
    """
    Optimizes ad spend and ROAS for a single ad campaign.
    Logs all actions, pauses campaign if budget or ROAS guardrails are breached.
    """

    def __init__(self, platform, campaign_id, session_id, budget_cfg):
        self.platform = platform        # 'meta_ads' or 'pinterest_ads'
        self.campaign_id = campaign_id
        self.session_id = session_id
        self.budget_cfg = budget_cfg
        self.paused = False            # Indicates if the campaign was paused
        self.logger = self._setup_logger()
        self.daily_spend = Decimal("0.00")
        self.daily_revenue = Decimal("0.00")
        self.last_reset = datetime.date.today()

    def _setup_logger(self):
        log_path = f'logs/ad_optimizer/{self.platform}_{self.campaign_id}.log'
        log_dir = os.path.dirname(log_path)
        os.makedirs(log_dir, exist_ok=True)

        logger_name = f'ad_optimizer.{self.platform}.{self.campaign_id}'
        logger = logging.getLogger(logger_name)

        # Prevent duplicate handlers (thread/process safe)
        if not any(isinstance(h, logging.FileHandler) and h.baseFilename == os.path.abspath(log_path)
                   for h in logger.handlers):
            handler = get_rotating_file_handler(log_path)
            formatter = logging.Formatter(
                f'[%(asctime)s] [SESSION:{self.session_id}] [%(levelname)s] %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        logger.setLevel(logging.INFO)
        return logger

    def reset_daily_counters(self):
        """Reset spend/revenue if the day changes."""
        if datetime.date.today() != self.last_reset:
            self.daily_spend = Decimal("0.00")
            self.daily_revenue = Decimal("0.00")
            self.last_reset = datetime.date.today()
            self.logger.info("Daily counters reset.")

    def track_spend(self, amount):
        """Add to spend, log, and check guardrails."""
        self.reset_daily_counters()
        self.daily_spend += Decimal(str(amount))
        self.logger.info(f"Tracked ad spend: ${amount}. Daily total: ${self.daily_spend}.")
        self._check_limits()

    def track_revenue(self, amount):
        """Add to attributed revenue, log, and check guardrails."""
        self.reset_daily_counters()
        self.daily_revenue += Decimal(str(amount))
        self.logger.info(f"Tracked attributed revenue: ${amount}. Daily total: ${self.daily_revenue}.")
        self._check_limits()

    def get_roas(self):
        """Return the current ROAS (Revenue / Ad Spend)."""
        if self.daily_spend > 0:
            return float(self.daily_revenue) / float(self.daily_spend)
        return 0.0

    def _check_limits(self):
        """Check both budget and ROAS. Pause if any guardrail is hit."""
        daily_budget = Decimal(str(self.budget_cfg.get('daily_budget_usd', 100)))
        min_roas = Decimal(str(self.budget_cfg.get('min_roas', 2.0)))

        if not check_budget_limit(self.platform, self.campaign_id, float(self.daily_spend), daily_budget):
            self.logger.warning(
                f"DAILY BUDGET EXCEEDED (${self.daily_spend} > ${daily_budget}) - Pausing campaign."
            )
            self.pause_campaign(reason="budget_exceeded")
            return

        roas = self.get_roas()
        if roas < float(min_roas) and self.daily_spend > 0:
            self.logger.warning(
                f"ROAS below minimum ({roas:.2f} < {min_roas}) - Pausing/optimizing campaign."
            )
            self.pause_campaign(reason="low_roas")

    def pause_campaign(self, reason):
        """Pause this ad campaign and log why."""
        self.paused = True
        self.logger.error(f"Paused campaign [{self.campaign_id}] on {self.platform} due to {reason}.")
        
        # Integrate API call to Meta/Pinterest to pause in real-time
        try:
            if self.platform == "meta_ads":
                from services.meta_ads_api import meta_api
                success = meta_api.pause_campaign(self.campaign_id)
                if success:
                    self.logger.info(f"Successfully paused Meta campaign {self.campaign_id}")
                else:
                    self.logger.error(f"Failed to pause Meta campaign {self.campaign_id}")
            elif self.platform == "pinterest_ads":
                from services.pinterest_ads_api import pinterest_api
                success = pinterest_api.pause_campaign(self.campaign_id)
                if success:
                    self.logger.info(f"Successfully paused Pinterest campaign {self.campaign_id}")
                else:
                    self.logger.error(f"Failed to pause Pinterest campaign {self.campaign_id}")
        except Exception as e:
            self.logger.error(f"Error pausing campaign via API: {e}")
        
        # TODO: Notify operator/Slack/email

    def summarize(self):
        """Return a summary dict for monitoring/dashboards."""
        return {
            "platform": self.platform,
            "campaign_id": self.campaign_id,
            "daily_spend": float(self.daily_spend),
            "daily_revenue": float(self.daily_revenue),
            "roas": self.get_roas(),
            "session_id": self.session_id,
            "paused": self.paused,
        }
