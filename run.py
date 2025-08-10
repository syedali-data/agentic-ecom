import os
import sys
import uuid
import logging
import json
from datetime import datetime
from dotenv import load_dotenv

# --- Add project root for robust imports ---
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from utils.log_rotation import get_rotating_file_handler

# --- Session ID Log Formatter ---
class SessionIDLogFormatter(logging.Formatter):
    def __init__(self, session_id, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.session_id = session_id

    def format(self, record):
        record.session_id = self.session_id
        return super().format(record)

# --- NDJSON event logger ---
def append_ndjson_log(log_path, data):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")

# --- Setup logging directories ---
os.makedirs("logs/controller", exist_ok=True)

# --- Generate Session/Run ID and set up logging ---
SESSION_ID = str(uuid.uuid4())
log_format = "%(asctime)s [%(levelname)s] [Session:%(session_id)s] %(message)s"
formatter = SessionIDLogFormatter(SESSION_ID, fmt=log_format)

# Rotating text log (readable)
file_handler = get_rotating_file_handler(
    "logs/controller/controller.log", when="midnight", backup_count=14
)
file_handler.setFormatter(formatter)

# Console log
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger = logging.getLogger("controller")
logger.setLevel(logging.INFO)
logger.handlers.clear()
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# NDJSON (JSON Lines) log for event/audit
NDJSON_PATH = "logs/controller/controller_events.ndjson"

def log_event(action, status="INFO", detail=None, **kwargs):
    event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "session_id": SESSION_ID,
        "level": status,
        "action": action,
        "detail": detail,
        **kwargs
    }
    append_ndjson_log(NDJSON_PATH, event)

# --- Load environment variables ---
load_dotenv()

# --- Import your project modules ---
from agents.sales_genie import generate_listing
from agents.logibot import LogiBot
from services.cj_api import fetch_mock_products
from services.shopify_api import create_product
from services.meta_ads_api import create_meta_ad

def is_kill_switch_on():
    return os.path.exists("status.lock")

def main():
    logger.info("Controller session started.")
    log_event("controller_start", status="INFO", detail="Controller session started.")
    if is_kill_switch_on():
        msg = "🚨 SYSTEM IS PAUSED BY KILL SWITCH (status.lock). No operations will be performed."
        print(msg)
        logger.warning(msg)
        log_event("kill_switch_engaged", status="WARNING", detail=msg)
        logger.info("Controller session finished (killed).")
        log_event("controller_finish", status="INFO", detail="Controller session finished (killed by kill switch).")
        return

    # -------- SALES GENIE: Product Research + Listing Generation + Shopify Post + Ads --------
    products = fetch_mock_products()
    listings = []

    for product in products:
        if is_kill_switch_on():
            logger.warning("Kill switch ON during product loop. Aborting workflow.")
            log_event("kill_switch_engaged", status="WARNING", detail="Aborted in product loop.")
            logger.info("Controller session finished (killed mid-product).")
            log_event("controller_finish", status="INFO", detail="Controller session finished (killed mid-product).")
            return

        print(f"\n=== Processing Product: {product['name']} ===")
        try:
            # 1. Generate compliant listing
            listing = generate_listing(product)
            if not listing:
                logger.info(f"Skipping product {product['name']} due to compliance or generation issue.")
                log_event("listing_skipped", status="INFO", detail="Compliance or generation issue", product=product['name'])
                continue

            # 2. POST TO SHOPIFY (LIVE)
            shopify_response = create_product(
                product["name"],
                listing,
                product["retail_price"],
                tags=product.get("tags"),
                images=product.get("images", [])
            )
            if shopify_response:
                logger.info(f"Posted to Shopify: {product['name']}")
                log_event("shopify_posted", status="INFO", product=product['name'])

                # --- Automatically launch Meta ads ---
                image_url = product.get("images", [""])[0]
                ad_budget = 20  # Default/demo budget

                try:
                    meta_ad_response = create_meta_ad(product["name"], listing, image_url, ad_budget)
                    if meta_ad_response["status"] == "success":
                        logger.info(f"[Meta] Ad created: {meta_ad_response['ad_id']}")
                        log_event("meta_ad_created", status="INFO", ad_id=meta_ad_response["ad_id"], product=product['name'])
                    else:
                        logger.error(f"[Meta] Ad creation failed for {product['name']}")
                        log_event("meta_ad_failed", status="ERROR", product=product['name'])
                except Exception as e:
                    logger.error(f"[Meta] Ad API Exception for {product['name']}: {e}")
                    log_event("meta_ad_exception", status="ERROR", detail=str(e), product=product['name'])



                listings.append({"product": product, "listing": listing})
            else:
                logger.error(f"❌ Shopify post failed: {product['name']}")
                log_event("shopify_post_failed", status="ERROR", product=product['name'])
            logger.info(f"Listing processed for {product['name']}")
            log_event("listing_processed", status="INFO", product=product['name'])
        except Exception as e:
            logger.error(f"Error generating or posting listing for {product['name']}: {e}")
            log_event("listing_exception", status="ERROR", detail=str(e), product=product['name'])

    # -------- LOGIBOT: Fulfillment, Tracking, Support --------
    logibot = LogiBot()
    for entry in listings:
        product = entry["product"]
        order_id = f"ORDER-{product['name'][:4].upper()}001"
        shipping_address = {"address1": "123 Main St", "city": "Toronto", "country": "CA"}

        if is_kill_switch_on():
            logger.warning("Kill switch ON during fulfillment loop. Aborting workflow.")
            log_event("kill_switch_engaged", status="WARNING", detail="Aborted in fulfillment loop.")
            logger.info("Controller session finished (killed mid-fulfillment).")
            log_event("controller_finish", status="INFO", detail="Controller session finished (killed mid-fulfillment).")
            return

        try:
            fulfill_result = logibot.fulfill_order(order_id, [{"sku": product.get("sku", "MOCKSKU"), "qty": 1}], shipping_address)
            print("Fulfillment Result:", fulfill_result)
            logger.info(f"Fulfillment Result for {order_id}: {fulfill_result}")
            log_event("fulfillment", status="INFO", order_id=order_id, result=fulfill_result)

            if fulfill_result.get("status") != "fulfilled":
                logger.error(f"Fulfillment failed for {order_id}: {fulfill_result.get('message')}")
                log_event("fulfillment_failed", status="ERROR", order_id=order_id, message=fulfill_result.get("message"))
                continue

            # Tracking
            tracking_result = logibot.get_tracking_info(fulfill_result["tracking_number"])
            print("Tracking Info:", tracking_result)
            logger.info(f"Tracking Info for {order_id}: {tracking_result}")
            log_event("tracking", status="INFO", order_id=order_id, result=tracking_result)

            # Support (example, can be conditional)
            support_result = logibot.handle_support_ticket({
                "ticket_id": f"TICKET-{order_id}",
                "customer_email": "customer@email.com",
                "message": f"Order update for {order_id}"
            })
            print("Support Ticket:", support_result)
            logger.info(f"Support Result for {order_id}: {support_result}")
            log_event("support", status="INFO", order_id=order_id, result=support_result)

        except Exception as e:
            logger.error(f"Error in LogiBot flow for {order_id}: {e}")
            log_event("logibot_exception", status="ERROR", order_id=order_id, detail=str(e))

    logger.info("Controller session finished.")
    log_event("controller_finish", status="INFO", detail="Controller session finished.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Uncaught exception in controller: {e}")
        log_event("controller_fatal", status="CRITICAL", detail=str(e))
        print("Fatal error occurred. Check logs for details.")
