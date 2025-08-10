"""
Sample data seeds for Agentic-Ecom database.
Provides test data for development and testing purposes.
"""

import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from db.models import (
    Product, Customer, Order, OrderItem, SupportTicket, 
    AdCampaign, InventoryItem, PricingHistory, AgentSession,
    AuditLog, EventLog, ProductStatus, OrderStatus, TicketStatus,
    TicketPriority, CampaignStatus, AgentType, EventType
)

def seed_sample_data(db: Session):
    """Seed the database with sample data."""
    
    print("🌱 Seeding sample data...")
    
    # Create sample products
    products = create_sample_products(db)
    
    # Create sample customers
    customers = create_sample_customers(db)
    
    # Create sample orders
    orders = create_sample_orders(db, customers, products)
    
    # Create sample support tickets
    tickets = create_sample_tickets(db, customers)
    
    # Create sample ad campaigns
    campaigns = create_sample_campaigns(db, products)
    
    # Create sample inventory
    inventory = create_sample_inventory(db, products)
    
    # Create sample pricing history
    pricing = create_sample_pricing_history(db, products)
    
    # Create sample agent sessions
    sessions = create_sample_agent_sessions(db)
    
    # Create sample audit logs
    audit_logs = create_sample_audit_logs(db)
    
    # Create sample event logs
    event_logs = create_sample_event_logs(db)
    
    print("✅ Sample data seeded successfully!")
    return {
        'products': len(products),
        'customers': len(customers),
        'orders': len(orders),
        'tickets': len(tickets),
        'campaigns': len(campaigns),
        'inventory': len(inventory),
        'pricing': len(pricing),
        'sessions': len(sessions),
        'audit_logs': len(audit_logs),
        'event_logs': len(event_logs)
    }

def create_sample_products(db: Session):
    """Create sample products."""
    products = [
        Product(
            name="Smart Fitness Tracker",
            description="Advanced fitness tracker with heart rate monitoring and GPS tracking",
            sku="FIT-001",
            category="Electronics",
            price=89.99,
            cost_price=45.00,
            status=ProductStatus.ACTIVE,
            image_url="https://example.com/fitness-tracker.jpg",
            supplier_id="SUP-001",
            supplier_name="TechSupplies Inc",
            tags=["fitness", "wearable", "health"],
            product_metadata={
                "brand": "FitTech",
                "warranty": "1 year",
                "battery_life": "7 days",
                "water_resistant": True
            },
            review_count=127,
            average_rating=4.5
        ),
        Product(
            name="LED Makeup Mirror",
            description="Professional LED makeup mirror with adjustable lighting",
            sku="BEAUTY-002",
            category="Beauty",
            price=149.99,
            cost_price=75.00,
            status=ProductStatus.ACTIVE,
            image_url="https://example.com/makeup-mirror.jpg",
            supplier_id="SUP-002",
            supplier_name="BeautySupplies Co",
            tags=["beauty", "mirror", "led"],
            product_metadata={
                "brand": "GlowMirror",
                "warranty": "2 years",
                "light_modes": 3,
                "magnification": "10x"
            },
            review_count=89,
            average_rating=4.7
        ),
        Product(
            name="Wireless Bluetooth Headphones",
            description="Premium wireless headphones with noise cancellation",
            sku="AUDIO-003",
            category="Electronics",
            price=199.99,
            cost_price=120.00,
            status=ProductStatus.ACTIVE,
            image_url="https://example.com/headphones.jpg",
            supplier_id="SUP-001",
            supplier_name="TechSupplies Inc",
            tags=["audio", "wireless", "bluetooth"],
            product_metadata={
                "brand": "SoundMax",
                "warranty": "1 year",
                "battery_life": "20 hours",
                "noise_cancellation": True
            },
            review_count=234,
            average_rating=4.6
        ),
        Product(
            name="Smart Coffee Maker",
            description="WiFi-enabled coffee maker with smartphone control",
            sku="HOME-004",
            category="Home & Kitchen",
            price=299.99,
            cost_price=180.00,
            status=ProductStatus.ACTIVE,
            image_url="https://example.com/coffee-maker.jpg",
            supplier_id="SUP-003",
            supplier_name="HomeGoods Ltd",
            tags=["coffee", "smart", "kitchen"],
            product_metadata={
                "brand": "BrewSmart",
                "warranty": "3 years",
                "capacity": "12 cups",
                "wifi_enabled": True
            },
            review_count=156,
            average_rating=4.4
        ),
        Product(
            name="Portable Power Bank",
            description="20000mAh portable charger with fast charging",
            sku="POWER-005",
            category="Electronics",
            price=49.99,
            cost_price=25.00,
            status=ProductStatus.ACTIVE,
            image_url="https://example.com/power-bank.jpg",
            supplier_id="SUP-001",
            supplier_name="TechSupplies Inc",
            tags=["power", "portable", "charging"],
            product_metadata={
                "brand": "PowerMax",
                "warranty": "1 year",
                "capacity": "20000mAh",
                "fast_charging": True
            },
            review_count=312,
            average_rating=4.8
        )
    ]
    
    for product in products:
        db.add(product)
    db.commit()
    
    print(f"✅ Created {len(products)} sample products")
    return products

def create_sample_customers(db: Session):
    """Create sample customers."""
    customers = [
        Customer(
            email="john.doe@example.com",
            first_name="John",
            last_name="Doe",
            phone="+1-555-0101",
            address={
                "street": "123 Main St",
                "city": "New York",
                "state": "NY",
                "zip": "10001",
                "country": "USA"
            },
            preferences={
                "newsletter": True,
                "marketing_emails": True,
                "preferred_categories": ["Electronics", "Home & Kitchen"]
            },
            total_orders=5,
            total_spent=899.95,
            last_order_date=datetime.now() - timedelta(days=7),
            is_active=True
        ),
        Customer(
            email="jane.smith@example.com",
            first_name="Jane",
            last_name="Smith",
            phone="+1-555-0102",
            address={
                "street": "456 Oak Ave",
                "city": "Los Angeles",
                "state": "CA",
                "zip": "90210",
                "country": "USA"
            },
            preferences={
                "newsletter": False,
                "marketing_emails": True,
                "preferred_categories": ["Beauty", "Fashion"]
            },
            total_orders=3,
            total_spent=449.97,
            last_order_date=datetime.now() - timedelta(days=14),
            is_active=True
        ),
        Customer(
            email="mike.wilson@example.com",
            first_name="Mike",
            last_name="Wilson",
            phone="+1-555-0103",
            address={
                "street": "789 Pine Rd",
                "city": "Chicago",
                "state": "IL",
                "zip": "60601",
                "country": "USA"
            },
            preferences={
                "newsletter": True,
                "marketing_emails": False,
                "preferred_categories": ["Electronics", "Sports"]
            },
            total_orders=8,
            total_spent=1599.92,
            last_order_date=datetime.now() - timedelta(days=2),
            is_active=True
        )
    ]
    
    for customer in customers:
        db.add(customer)
    db.commit()
    
    print(f"✅ Created {len(customers)} sample customers")
    return customers

def create_sample_orders(db: Session, customers, products):
    """Create sample orders."""
    orders = []
    
    # Order 1
    order1 = Order(
        order_number="ORD-2024-001",
        customer_id=customers[0].id,
        status=OrderStatus.DELIVERED,
        subtotal=89.99,
        tax=7.20,
        shipping=5.99,
        total=103.18,
        currency="USD",
        shipping_address=customers[0].address,
        billing_address=customers[0].address,
        payment_method="credit_card",
        payment_status="paid",
        tracking_number="TRK123456789",
        notes="Customer requested signature delivery"
    )
    db.add(order1)
    db.flush()
    
    order_item1 = OrderItem(
        order_id=order1.id,
        product_id=products[0].id,
        quantity=1,
        unit_price=89.99,
        total_price=89.99
    )
    db.add(order_item1)
    orders.append(order1)
    
    # Order 2
    order2 = Order(
        order_number="ORD-2024-002",
        customer_id=customers[1].id,
        status=OrderStatus.SHIPPED,
        subtotal=149.99,
        tax=12.00,
        shipping=0.00,
        total=161.99,
        currency="USD",
        shipping_address=customers[1].address,
        billing_address=customers[1].address,
        payment_method="paypal",
        payment_status="paid",
        tracking_number="TRK987654321"
    )
    db.add(order2)
    db.flush()
    
    order_item2 = OrderItem(
        order_id=order2.id,
        product_id=products[1].id,
        quantity=1,
        unit_price=149.99,
        total_price=149.99
    )
    db.add(order_item2)
    orders.append(order2)
    
    db.commit()
    print(f"✅ Created {len(orders)} sample orders")
    return orders

def create_sample_tickets(db: Session, customers):
    """Create sample support tickets."""
    tickets = [
        SupportTicket(
            ticket_number="TKT-2024-001",
            customer_id=customers[0].id,
            subject="Order delivery question",
            description="I ordered a fitness tracker last week and haven't received it yet. Can you help me track it?",
            status=TicketStatus.RESOLVED,
            priority=TicketPriority.MEDIUM,
            assigned_agent="support_agent_1",
            category="order_inquiry",
            tags=["delivery", "tracking"],
            resolution="Order was delivered on time. Customer was not home for signature delivery. Arranged redelivery.",
            resolved_at=datetime.now() - timedelta(days=1)
        ),
        SupportTicket(
            ticket_number="TKT-2024-002",
            customer_id=customers[1].id,
            subject="Product defect",
            description="The LED mirror I received has a scratch on the surface. Can I get a replacement?",
            status=TicketStatus.IN_PROGRESS,
            priority=TicketPriority.HIGH,
            assigned_agent="support_agent_2",
            category="product_issue",
            tags=["defect", "replacement"]
        )
    ]
    
    for ticket in tickets:
        db.add(ticket)
    db.commit()
    
    print(f"✅ Created {len(tickets)} sample support tickets")
    return tickets

def create_sample_campaigns(db: Session, products):
    """Create sample ad campaigns."""
    campaigns = [
        AdCampaign(
            name="Fitness Tracker Summer Sale",
            platform="facebook",
            status=CampaignStatus.ACTIVE,
            budget=500.00,
            daily_budget=50.00,
            start_date=datetime.now() - timedelta(days=7),
            end_date=datetime.now() + timedelta(days=23),
            target_audience={
                "age_range": "25-45",
                "interests": ["fitness", "health", "technology"],
                "location": "United States"
            },
            ad_creative={
                "headline": "Track Your Fitness Goals",
                "description": "Advanced fitness tracker with heart rate monitoring",
                "image_url": "https://example.com/fitness-ad.jpg"
            },
            metrics={
                "impressions": 15000,
                "clicks": 450,
                "conversions": 23,
                "spend": 245.50
            },
            product_id=products[0].id
        ),
        AdCampaign(
            name="Beauty Mirror Promotion",
            platform="pinterest",
            status=CampaignStatus.ACTIVE,
            budget=300.00,
            daily_budget=30.00,
            start_date=datetime.now() - timedelta(days=3),
            end_date=datetime.now() + timedelta(days=27),
            target_audience={
                "age_range": "18-35",
                "interests": ["beauty", "makeup", "fashion"],
                "location": "United States"
            },
            ad_creative={
                "headline": "Professional Makeup Mirror",
                "description": "LED mirror with adjustable lighting",
                "image_url": "https://example.com/mirror-ad.jpg"
            },
            metrics={
                "impressions": 8000,
                "clicks": 280,
                "conversions": 15,
                "spend": 120.75
            },
            product_id=products[1].id
        )
    ]
    
    for campaign in campaigns:
        db.add(campaign)
    db.commit()
    
    print(f"✅ Created {len(campaigns)} sample ad campaigns")
    return campaigns

def create_sample_inventory(db: Session, products):
    """Create sample inventory items."""
    inventory = []
    
    for product in products:
        inventory_item = InventoryItem(
            product_id=product.id,
            quantity=100,
            reserved_quantity=5,
            available_quantity=95,
            low_stock_threshold=10,
            supplier_stock=500
        )
        db.add(inventory_item)
        inventory.append(inventory_item)
    
    db.commit()
    print(f"✅ Created {len(inventory)} sample inventory items")
    return inventory

def create_sample_pricing_history(db: Session, products):
    """Create sample pricing history."""
    pricing = []
    
    for product in products:
        # Create a few price changes for each product
        for i in range(3):
            old_price = product.price - (i * 5)
            new_price = product.price - ((i + 1) * 5)
            
            pricing_entry = PricingHistory(
                product_id=product.id,
                old_price=old_price,
                new_price=new_price,
                change_reason="Competitive pricing adjustment",
                change_type="automatic"
            )
            db.add(pricing_entry)
            pricing.append(pricing_entry)
    
    db.commit()
    print(f"✅ Created {len(pricing)} sample pricing history entries")
    return pricing

def create_sample_agent_sessions(db: Session):
    """Create sample agent sessions."""
    sessions = [
        AgentSession(
            session_id="session_sales_genie_001",
            agent_type=AgentType.SALES_GENIE,
            status="completed",
            start_time=datetime.now() - timedelta(hours=2),
            end_time=datetime.now() - timedelta(hours=1),
            duration_seconds=3600,
            tasks_completed=15,
            errors_count=0,
            session_metadata={
                "products_processed": 5,
                "ads_created": 3,
                "campaigns_launched": 2
            }
        ),
        AgentSession(
            session_id="session_logibot_001",
            agent_type=AgentType.LOGIBOT,
            status="active",
            start_time=datetime.now() - timedelta(minutes=30),
            end_time=None,
            duration_seconds=1800,
            tasks_completed=8,
            errors_count=1,
            session_metadata={
                "tickets_processed": 5,
                "orders_fulfilled": 3,
                "fraud_checks": 12
            }
        )
    ]
    
    for session in sessions:
        db.add(session)
    db.commit()
    
    print(f"✅ Created {len(sessions)} sample agent sessions")
    return sessions

def create_sample_audit_logs(db: Session):
    """Create sample audit logs."""
    audit_logs = [
        AuditLog(
            user_id="admin_user",
            action="product_created",
            resource_type="product",
            resource_id="prod_001",
            old_values=None,
            new_values={"name": "Smart Fitness Tracker", "price": 89.99},
            ip_address="192.168.1.100",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        ),
        AuditLog(
            user_id="sales_agent",
            action="price_updated",
            resource_type="product",
            resource_id="prod_001",
            old_values={"price": 89.99},
            new_values={"price": 84.99},
            ip_address="192.168.1.101",
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
    ]
    
    for log in audit_logs:
        db.add(log)
    db.commit()
    
    print(f"✅ Created {len(audit_logs)} sample audit logs")
    return audit_logs

def create_sample_event_logs(db: Session):
    """Create sample event logs."""
    event_logs = [
        EventLog(
            event_type=EventType.PRODUCT_CREATED,
            source="sales_genie",
            data={
                "product_id": "prod_001",
                "product_name": "Smart Fitness Tracker",
                "agent_session": "session_sales_genie_001"
            },
            processed=True
        ),
        EventLog(
            event_type=EventType.ORDER_PLACED,
            source="api",
            data={
                "order_id": "ord_001",
                "customer_id": "cust_001",
                "total_amount": 103.18
            },
            processed=True
        ),
        EventLog(
            event_type=EventType.AD_CAMPAIGN_LAUNCHED,
            source="sales_genie",
            data={
                "campaign_id": "camp_001",
                "platform": "facebook",
                "budget": 500.00
            },
            processed=False
        )
    ]
    
    for log in event_logs:
        db.add(log)
    db.commit()
    
    print(f"✅ Created {len(event_logs)} sample event logs")
    return event_logs 