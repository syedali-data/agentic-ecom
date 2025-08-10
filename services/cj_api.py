from typing import List, Dict
from utils.retry_utils import retry  # ✅ Add this import

# Simulated product list
MOCK_PRODUCTS = [
    {
        "id": "p001",
        "name": "Smart Fitness Tracker",
        "cost": 12.00,
        "retail_price": 39.99,
        "shipping_time_days": 7,
        "rating": 4.6,
        "reviews": 127,
        "inventory": 320,
        "tags": ["fitness", "tech", "wearable"],
        "images": ["https://plus.unsplash.com/premium_photo-1681433383783-661b519b154a?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8c21hcnQlMjBmaXRuZXNzJTIwdHJhY2tlcnxlbnwwfHwwfHx8MA%3D%3D"]
    },
    {
        "id": "p002",
        "name": "LED Makeup Mirror",
        "cost": 6.50,
        "retail_price": 24.99,
        "shipping_time_days": 9,
        "rating": 4.3,
        "reviews": 54,
        "inventory": 85,
        "tags": ["beauty", "gadget", "vanity"],
        "images": ["https://images.unsplash.com/photo-1506744038136-46273834b3fb"]
    },
    {
        "id": "p003",
        "name": "Basic Coffee Mug",
        "category": "kitchen",
        "cost": 5.00,
        "retail_price": 15.00,
        "shipping_time_days": 5,
        "rating": 4.6,
        "reviews": 200,
        "inventory": 300,
        "tags": ["mug", "kitchen", "coffee"],
        "images": ["https://media.istockphoto.com/id/2175888310/photo/enjoy-coffee.jpg?s=1024x1024&w=is&k=20&c=VIqqYqMz8Ry3T-6oP0duSTi2XLNdMwDUYPWf7RthQhs="]
    }
]


@retry(max_attempts=3)   # ✅ Resilient wrapper added
def fetch_mock_products() -> List[Dict]:
    print("[CJ API] Pulling mock product list...")
    return MOCK_PRODUCTS

def score_product(product: Dict) -> float:
    margin = (product['retail_price'] - product['cost']) / product['cost']
    rating_score = product['rating'] / 5
    review_score = min(product['reviews'], 300) / 300
    inventory_score = min(product['inventory'], 300) / 300
    shipping_penalty = 1 if product['shipping_time_days'] <= 10 else 0.8

    score = (margin * 0.35 +
             rating_score * 0.25 +
             review_score * 0.2 +
             inventory_score * 0.1 +
             shipping_penalty * 0.1)

    return round(score, 3)

def get_top_products(limit: int = 3) -> List[Dict]:
    products = fetch_mock_products()
    for product in products:
        product['score'] = score_product(product)
    sorted_products = sorted(products, key=lambda x: x['score'], reverse=True)
    return sorted_products[:limit]

def post_all_products():
    from services.shopify_api import create_product

    products = fetch_mock_products()
    for p in products:
        print(f"Posting: {p['name']} (ID: {p['id']})")
        result = create_product(
            title=p["name"],
            body_html=f"Auto description for {p['name']}",
            price=p["retail_price"],
            tags=p.get("tags", []),
            images=p.get("images", [])
        )
        if result:
            print(f"✅ Posted: {p['name']}")
        else:
            print(f"❌ Failed to post: {p['name']}")

if __name__ == "__main__":
    print("Product Scores (for debugging):")
    all_products = fetch_mock_products()
    for p in all_products:
        print(f"{p['name']}: score={score_product(p)}")

    print("\nPosting ALL products to Shopify:")
    post_all_products()
