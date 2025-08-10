import os
import requests
from dotenv import load_dotenv
from utils.retry_utils import retry
import logging

# --- 1. Load .env variables from project root ---
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")
SHOPIFY_STORE_DOMAIN = os.getenv("SHOPIFY_STORE_DOMAIN")

logger = logging.getLogger(__name__)

logger.debug("Shopify store domain configured")
logger.debug("Shopify access token configured")

# --- 2. Retry decorator (adjust max_attempts as needed) ---
@retry(max_attempts=5, delay=2)
def create_product(title, body_html, price, tags=None, images=None):
    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/2024-04/products.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
    }
    product_data = {
        "product": {
            "title": title,
            "body_html": body_html,
            "vendor": "Agentic-Ecom",
            "tags": tags or [],
            "images": [{"src": img_url} for img_url in (images or [])],
            "variants": [
                {
                    "price": str(price),
                    "sku": title.replace(" ", "-")[:20],
                }
            ]
        }
    }
    try:
        response = requests.post(url, headers=headers, json=product_data)
        if response.status_code == 201:
            print(f"✅ Shopify: Posted '{title}' successfully!")
            return response.json()
        else:
            print(f"❌ Shopify Error: {response.status_code}, {response.text}")
            # Raise to trigger retry
            raise Exception(f"Shopify post failed: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Exception posting to Shopify: {e}")
        raise  # Will be handled by retry decorator

@retry(max_attempts=5, delay=2)
def get_products(limit=50, status="active"):
    """
    Retrieve products from Shopify store
    
    Args:
        limit: Number of products to retrieve (max 250)
        status: Product status filter (active, archived, draft)
        
    Returns:
        List of products or empty list if error
    """
    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/2024-04/products.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
    }
    params = {
        "limit": min(limit, 250),  # Shopify max is 250
        "status": status
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            products = data.get("products", [])
            print(f"✅ Shopify: Retrieved {len(products)} products successfully!")
            return products
        else:
            print(f"❌ Shopify Error: {response.status_code}, {response.text}")
            return []
    except Exception as e:
        print(f"Exception retrieving products from Shopify: {e}")
        return []

@retry(max_attempts=5, delay=2)
def get_product_by_id(product_id):
    """
    Retrieve a specific product by ID
    
    Args:
        product_id: Shopify product ID
        
    Returns:
        Product data or None if error
    """
    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/2024-04/products/{product_id}.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            product = data.get("product")
            print(f"✅ Shopify: Retrieved product {product_id} successfully!")
            return product
        else:
            print(f"❌ Shopify Error: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Exception retrieving product {product_id} from Shopify: {e}")
        return None

