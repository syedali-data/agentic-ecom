import yaml

def load_budget_config(path='config/budget_limits.yaml'):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def get_campaign_budget_config(platform, campaign_id, config):
    platform_cfg = config.get(platform, {})
    campaign_cfg = platform_cfg.get('campaigns', {}).get(campaign_id)
    if campaign_cfg:
        return campaign_cfg
    return platform_cfg.get('default', {})
