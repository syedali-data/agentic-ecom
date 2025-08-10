import sys
import os
import uuid
import logging
from dotenv import load_dotenv

# --- Add project root for imports ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.log_rotation import get_rotating_file_handler
from utils.config_loader import load_budget_config, get_campaign_budget_config
from services.compliance import check_text_compliance, check_category_compliance
from logs.notion_logger import log_action
from openai import OpenAI
from services.cj_api import fetch_mock_products
from services.shopify_api import create_product
from services.ad_optimizer import AdOptimizer
from services.meta_ads_api import launch_meta_ad_campaign, get_meta_ad_metrics
from services.pinterest_ads_api import launch_pinterest_ad_campaign, get_pinterest_ad_metrics
from utils.safety_manager import safety_manager, require_safety_check
from analytics.viral_trend_analyzer import ViralTrendAnalyzer
from db.database import get_db

# --- Session/Run ID Logging Formatter ---
class SessionIDLogFormatter(logging.Formatter):
    def __init__(self, session_id, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.session_id = session_id
    def format(self, record):
        record.session_id = self.session_id
        return super().format(record)

SESSION_ID = str(uuid.uuid4())
log_format = "%(asctime)s [%(levelname)s] [Session:%(session_id)s] %(message)s"
formatter = SessionIDLogFormatter(SESSION_ID, fmt=log_format)

os.makedirs("logs/sales_genie", exist_ok=True)
log_path = "logs/sales_genie/sales_genie.log"

# --- Logger Setup ---
logger = logging.getLogger("salesgenie")
logger.setLevel(logging.INFO)
if not logger.handlers:
    file_handler = get_rotating_file_handler(log_path, when="midnight", backup_count=14)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

# Always load .env from project root!
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

logger.info("SalesGenie session started.")
logger.debug("Shopify store domain configured")
logger.debug("Shopify access token configured")
logger.info("OpenAI API client initialized successfully")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def is_kill_switch_on():
    root = os.path.dirname(os.path.dirname(__file__))
    return os.path.exists(os.path.join(root, "status.lock"))

def discover_viral_products(categories=None, max_products=20, min_viral_score=0.6):
    """
    Discover viral products using AI-powered trend analysis.
    
    Args:
        categories: List of categories to analyze (None for all)
        max_products: Maximum number of products to return
        min_viral_score: Minimum viral score threshold
        
    Returns:
        List of viral product candidates
    """
    try:
        logger.info(f"Starting viral product discovery for categories: {categories}")
        print(f"\n🔍 Discovering viral products for categories: {categories or 'all'}")
        
        # Initialize viral trend analyzer
        db = get_db()
        viral_analyzer = ViralTrendAnalyzer(db)
        
        # Discover viral products
        discovery_results = viral_analyzer.discover_viral_products(
            categories=categories,
            max_products=max_products,
            min_viral_score=min_viral_score,
            include_analysis=True
        )
        
        if "error" in discovery_results:
            logger.error(f"Error in viral product discovery: {discovery_results['error']}")
            print(f"❌ Error discovering viral products: {discovery_results['error']}")
            return []
        
        viral_products = discovery_results.get("viral_products", [])
        
        logger.info(f"Discovered {len(viral_products)} viral products")
        print(f"✅ Discovered {len(viral_products)} viral products")
        
        # Log discovery summary
        summary = discovery_results.get("summary", {})
        print(f"   📊 High potential: {summary.get('high_potential', 0)}")
        print(f"   📊 Medium potential: {summary.get('medium_potential', 0)}")
        print(f"   📊 Low risk: {summary.get('low_risk', 0)}")
        
        # Show top products
        if viral_products:
            print(f"\n   🎯 Top Viral Products:")
            for i, product in enumerate(viral_products[:5], 1):
                print(f"   {i}. {product['product_name']} (Score: {product['viral_score']:.2f}, Risk: {product['risk_level']})")
        
        return viral_products
        
    except Exception as e:
        logger.error(f"Error in viral product discovery: {e}")
        print(f"❌ Error discovering viral products: {e}")
        return []

def analyze_product_viral_potential(product_name, category=None):
    """
    Analyze viral potential for a specific product.
    
    Args:
        product_name: Name of the product to analyze
        category: Product category (optional)
        
    Returns:
        Viral potential analysis
    """
    try:
        logger.info(f"Analyzing viral potential for: {product_name}")
        print(f"\n🔍 Analyzing viral potential for: {product_name}")
        
        # Initialize viral trend analyzer
        db = get_db()
        viral_analyzer = ViralTrendAnalyzer(db)
        
        # Analyze product viral potential
        analysis = viral_analyzer.analyze_product_viral_potential(product_name, category)
        
        if "error" in analysis:
            logger.error(f"Error analyzing product viral potential: {analysis['error']}")
            print(f"❌ Error analyzing product: {analysis['error']}")
            return None
        
        # Log analysis results
        print(f"✅ Analysis completed")
        print(f"   Viral Score: {analysis['viral_score']:.2f}")
        print(f"   Market Potential: {analysis['market_potential']:.2f}")
        print(f"   Competition Level: {analysis['competition_level']}")
        print(f"   Risk Level: {analysis['risk_level']}")
        
        # Show recommendations
        if analysis.get('recommendations'):
            print(f"   📋 Recommendations:")
            for rec in analysis['recommendations'][:3]:
                print(f"     - {rec}")
        
        return analysis
        
    except Exception as e:
        logger.error(f"Error analyzing product viral potential: {e}")
        print(f"❌ Error analyzing product: {e}")
        return None

def format_prompt(product):
    return f"""
You are a helpful e-commerce copywriter. Write a Shopify-ready product title and description for the following product.

Rules:
- Be clear and engaging
- Do not exaggerate or make false claims
- Include the use case and key features
- Format with short paragraphs and bullet points

Product Info:
Name: {product['name']}
Cost: ${product['cost']}
Retail Price: ${product['retail_price']}
Shipping: {product['shipping_time_days']} days
Rating: {product['rating']}
Tags: {', '.join(product['tags'])}
"""

def generate_listing(product):
    prompt = format_prompt(product)
    logger.info(f"Generating listing for: {product['name']}")
    print(f"\n🔍 Generating copy for: {product['name']}")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        result = response.choices[0].message.content
        logger.info(f"LLM copy generated for {product['name']}")
        print("DEBUG: GPT OUTPUT:", result)

        # COMPLIANCE CHECK ON TEXT
        compliant, reason = check_text_compliance(result)
        if not compliant:
            print(f"🚫 Compliance warning: {reason}")
            logger.warning(f"TextComplianceFailure | {reason} | Product: {product['name']}")
            log_action("SalesGenie", "TextComplianceFailure", reason, level="WARNING", product_name=product["name"])
            return None

        print(f"📝 Generated Listing:\n{result}\n")
        logger.info(f"Listing generated for: {product['name']}")
        return result
    except Exception as e:
        logger.error(f"Error generating listing for {product['name']}: {e}")
        return None

def post_shopify_listing(product, listing):
    try:
        shopify_response = create_product(
            product["name"],
            listing,
            product["retail_price"],
            tags=product.get("tags"),
            images=product.get("images", [])
        )
        if shopify_response:
            logger.info(f"Posted to Shopify: {product['name']}")
            log_action("SalesGenie", "ListingPosted", "Product successfully posted!", level="INFO", product_name=product["name"])
            return True
        else:
            logger.error(f"ShopifyError | Failed to post product | Product: {product['name']}")
            log_action("SalesGenie", "ShopifyError", "Failed to post product.", level="ERROR", product_name=product["name"])
            return False
    except Exception as e:
        logger.error(f"Exception posting to Shopify for {product['name']}: {e}")
        return False

@require_safety_check("launch_ad_campaign", "meta_ads")
def launch_and_optimize_ad(product, platform, campaign_id, session_id):
    """
    Launches an ad campaign (Meta or Pinterest), tracks spend/revenue, and runs optimizer.
    """
    # Safety check for campaign creation
    if not safety_manager.track_campaign_creation(platform):
        logger.warning(f"Campaign creation blocked for {platform}")
        return
    
    budget_config = load_budget_config()
    budget_cfg = get_campaign_budget_config(platform, campaign_id, budget_config)

    # --- Launch Ad Campaign and Get Metrics ---
    if platform == "meta_ads":
        launch_meta_ad_campaign(product, campaign_id)
        spend, revenue = get_meta_ad_metrics(campaign_id)
    elif platform == "pinterest_ads":
        launch_pinterest_ad_campaign(product, campaign_id)
        spend, revenue = get_pinterest_ad_metrics(campaign_id)
    else:
        spend = revenue = 0

    # Safety check for spend tracking
    if not safety_manager.track_spend(spend, platform):
        logger.warning(f"Spend tracking blocked for {platform}")
        return

    optimizer = AdOptimizer(
        platform=platform,
        campaign_id=campaign_id,
        session_id=session_id,
        budget_cfg=budget_cfg
    )
    optimizer.track_spend(spend)
    optimizer.track_revenue(revenue)
    summary = optimizer.summarize()
    logger.info(f"Ad Campaign Summary: {summary}")

def main():
    if is_kill_switch_on():
        print("🚨 System is paused by kill switch (status.lock). No operations will be performed.")
        logger.warning("Kill switch is ON. SalesGenie session aborted.")
        exit(0)

    print("🚀 SalesGenie - AI-Powered Product Discovery & Marketing")
    print("=" * 60)
    
    # Step 1: Discover viral products using AI-powered trend analysis
    print("\n🔍 STEP 1: AI-Powered Viral Product Discovery")
    print("-" * 40)
    
    viral_products = discover_viral_products(
        categories=["electronics", "fashion", "home", "beauty", "fitness"],
        max_products=10,
        min_viral_score=0.6
    )
    
    if not viral_products:
        print("⚠️ No viral products discovered. Falling back to mock products.")
        products = fetch_mock_products()
    else:
        print(f"✅ Discovered {len(viral_products)} viral products")
        
        # Convert viral products to the format expected by the rest of the pipeline
        products = []
        for viral_product in viral_products[:5]:  # Limit to top 5 viral products
            # Create product object from viral product data
            product = {
                "name": viral_product["product_name"],
                "category": viral_product["category"],
                "cost": 15.0,  # Default cost
                "retail_price": 29.99,  # Default retail price
                "shipping_time_days": 7,
                "rating": 4.5,
                "tags": ["viral", "trending", viral_product["category"]],
                "viral_score": viral_product["viral_score"],
                "market_potential": viral_product["market_potential"],
                "risk_level": viral_product["risk_level"]
            }
            products.append(product)
    
    print(f"\n📦 Processing {len(products)} products...")
    
    # Step 2: Process each product
    for idx, product in enumerate(products):
        print(f"\n{'='*50}")
        print(f"Processing Product {idx+1}/{len(products)}: {product['name']}")
        print(f"{'='*50}")
        
        # Check if this is a viral product
        if "viral_score" in product:
            print(f"🎯 Viral Score: {product['viral_score']:.2f}")
            print(f"🎯 Market Potential: {product['market_potential']:.2f}")
            print(f"🎯 Risk Level: {product['risk_level']}")
            
            # Analyze viral potential in detail
            viral_analysis = analyze_product_viral_potential(product['name'], product['category'])
            if viral_analysis:
                print(f"📊 Detailed Analysis: {viral_analysis['viral_score']:.2f} viral score")
        
        # 1. Category compliance check
        compliant, reason = check_category_compliance(product.get("category", ""))
        if not compliant:
            print(f"🚫 Category not allowed: {reason}")
            logger.warning(f"CategoryComplianceFailure | {reason} | Product: {product['name']}")
            log_action("SalesGenie", "CategoryComplianceFailure", reason, level="ERROR", product_name=product["name"])
            continue

        # 2. Listing generation + text compliance
        listing = generate_listing(product)
        if listing is None:
            continue

        # 3. Post to Shopify
        if not post_shopify_listing(product, listing):
            continue

        # 4. Launch and optimize ad campaigns (Meta & Pinterest)
        meta_campaign_id = f"meta_{idx+1}_{product['name'].replace(' ','_')}"
        pinterest_campaign_id = f"pinterest_{idx+1}_{product['name'].replace(' ','_')}"

        launch_and_optimize_ad(product, "meta_ads", meta_campaign_id, SESSION_ID)
        launch_and_optimize_ad(product, "pinterest_ads", pinterest_campaign_id, SESSION_ID)

    print(f"\n✅ SalesGenie session completed successfully!")
    print(f"📊 Processed {len(products)} products")
    logger.info("SalesGenie session finished.")

if __name__ == "__main__":
    main()
