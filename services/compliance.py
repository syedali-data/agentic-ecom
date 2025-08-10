import yaml
import re

COMPLIANCE_YAML_PATH = "config/compliance_rules.yaml"

def load_rules():
    with open(COMPLIANCE_YAML_PATH, "r") as file:
        return yaml.safe_load(file)

def check_text_compliance(text, rules=None):
    if rules is None:
        rules = load_rules()
    for banned in rules.get("banned_keywords", []):
        # Regex: match whole word (case-insensitive)
        pattern = r'\b' + re.escape(banned) + r'\b'
        if re.search(pattern, text, flags=re.IGNORECASE):
            return False, f"Banned keyword detected: {banned}"
    return True, ""

def check_category_compliance(category, region="canada", rules=None):
    if rules is None:
        rules = load_rules()
    banned = rules.get("regions", {}).get(region, {}).get("banned_product_categories", [])
    if category.lower() in [b.lower() for b in banned]:
        return False, f"Product category '{category}' is not allowed in {region.title()}"
    return True, ""
