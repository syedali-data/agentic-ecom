# services/budget_guard.py

def check_budget_limit(platform, campaign_id, current_spend, daily_budget):
    return current_spend <= daily_budget
