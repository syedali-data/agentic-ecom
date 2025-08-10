# 🗄️ Database System Documentation

## Overview

The Agentic-Ecom database system provides a comprehensive data layer using SQLAlchemy ORM with PostgreSQL support and SQLite fallback for development. The system includes 11 core tables covering all aspects of e-commerce operations.

## 🏗️ Architecture

### Database Layer
- **SQLAlchemy ORM**: Object-relational mapping for type-safe database operations
- **PostgreSQL**: Primary database for production (scalable, ACID compliant)
- **SQLite**: Development fallback (file-based, no setup required)
- **Connection Pooling**: Efficient connection management
- **Migration System**: Alembic-based schema versioning

### Core Tables

| Table | Purpose | Key Features |
|-------|---------|--------------|
| `products` | Product catalog | Metadata, reviews, pricing history |
| `customers` | Customer management | Preferences, order history, addresses |
| `orders` | Order processing | Status tracking, payment info |
| `order_items` | Order line items | Product quantities, pricing |
| `support_tickets` | Customer support | Priority, status, resolution tracking |
| `ad_campaigns` | Advertising campaigns | Multi-platform, metrics, targeting |
| `inventory_items` | Stock management | Quantity tracking, low stock alerts |
| `pricing_history` | Price changes | Audit trail, change reasons |
| `agent_sessions` | AI agent monitoring | Performance tracking, session data |
| `audit_logs` | System audit trail | Change tracking, compliance |
| `event_logs` | Business events | Event processing, analytics |

## 🚀 Quick Start

### 1. Initialize Database
```bash
# Create tables
python db/init_database.py --action init

# Seed with sample data
python db/init_database.py --action seed

# Full setup (init + seed)
python db/init_database.py --action full-setup
```

### 2. Check Database Status
```bash
python db/init_database.py --action info
```

### 3. Reset Database (Development)
```bash
python db/init_database.py --action reset
```

## 📊 Database Models

### Product Model
```python
class Product(BaseModel):
    name: str                    # Product name
    description: str             # Product description
    sku: str                     # Stock keeping unit
    category: str                # Product category
    price: float                 # Current price
    cost_price: float            # Cost price
    status: ProductStatus        # Active/Inactive/Discontinued
    tags: List[str]              # Product tags
    product_metadata: Dict       # Additional product data
    review_count: int            # Number of reviews
    average_rating: float        # Average rating
```

### Customer Model
```python
class Customer(BaseModel):
    email: str                   # Unique email
    first_name: str              # First name
    last_name: str               # Last name
    address: Dict                # Shipping/billing address
    preferences: Dict            # Customer preferences
    total_orders: int            # Order count
    total_spent: float           # Total spending
    is_active: bool              # Account status
```

### Order Model
```python
class Order(BaseModel):
    order_number: str            # Unique order number
    customer_id: str             # Customer reference
    status: OrderStatus          # Order status
    subtotal: float              # Order subtotal
    tax: float                   # Tax amount
    shipping: float              # Shipping cost
    total: float                 # Total amount
    payment_method: str          # Payment method
    tracking_number: str         # Shipping tracking
```

## 🔧 Database Service

The `DatabaseService` class provides high-level operations:

```python
from services.db_service import DatabaseService
from db.database import get_db

# Get database session
db = next(get_db())
db_service = DatabaseService(db)

# Product operations
product = db_service.create_product(product_data)
products = db_service.get_products(category="Electronics")
product = db_service.update_product(product_id, update_data)

# Customer operations
customer = db_service.create_customer(customer_data)
customer = db_service.get_customer_by_email(email)

# Order operations
order = db_service.create_order(order_data, order_items)
orders = db_service.get_orders_by_customer(customer_id)

# Analytics
analytics = db_service.get_sales_analytics(days=30)
customer_analytics = db_service.get_customer_analytics()
```

## 📈 Analytics & Reporting

### Sales Analytics
```python
analytics = db_service.get_sales_analytics(days=30)
# Returns:
{
    "period_days": 30,
    "total_orders": 150,
    "total_revenue": 15000.00,
    "average_order_value": 100.00,
    "orders_by_status": {
        "delivered": 120,
        "shipped": 20,
        "pending": 10
    },
    "top_products": [...]
}
```

### Customer Analytics
```python
customer_analytics = db_service.get_customer_analytics()
# Returns:
{
    "total_customers": 500,
    "active_customers": 450,
    "inactive_customers": 50,
    "top_customers": [...]
}
```

## 🔍 Query Examples

### Complex Queries
```python
# Get products with low stock
low_stock = db_service.get_low_stock_products()

# Get tickets by priority
high_priority_tickets = db_service.get_tickets_by_priority(TicketPriority.HIGH)

# Get orders by status
pending_orders = db.query(Order).filter(Order.status == OrderStatus.PENDING).all()

# Get customer with most orders
top_customer = db.query(Customer).order_by(desc(Customer.total_orders)).first()
```

### Filtering and Sorting
```python
# Products in Electronics category, active status, price range
products = db_service.get_products(
    category="Electronics",
    status=ProductStatus.ACTIVE,
    min_price=50.0,
    max_price=200.0,
    limit=20
)
```

## 🔐 Security & Audit

### Audit Logging
All database changes are automatically logged:

```python
# Automatic audit logging on product updates
product = db_service.update_product(product_id, {"price": 99.99})
# Creates audit log entry with old/new values
```

### Event Logging
Business events are tracked for analytics:

```python
# Automatic event logging on order creation
order = db_service.create_order(order_data, order_items)
# Creates event log entry for ORDER_PLACED
```

## 🚀 Performance Optimization

### Indexes
The database includes optimized indexes:
- Primary keys on all tables
- Foreign key indexes
- Composite indexes for common queries
- Full-text search indexes (PostgreSQL)

### Connection Pooling
- Configurable pool size
- Connection recycling
- Health checks
- Timeout handling

### Query Optimization
```python
# Use specific columns instead of SELECT *
products = db.query(Product.id, Product.name, Product.price).all()

# Use joins for related data
orders_with_customers = db.query(Order).join(Customer).all()

# Use pagination for large datasets
products = db.query(Product).offset(0).limit(20).all()
```

## 🔄 Migrations

### Creating Migrations
```bash
# Generate migration (when using Alembic)
alembic revision --autogenerate -m "Add new field"

# Apply migrations
alembic upgrade head
```

### Migration Best Practices
- Always backup before migrations
- Test migrations on staging
- Use transactions for safety
- Document breaking changes

## 🛠️ Maintenance

### Database Health Checks
```python
from db.database import health_check

health = health_check()
print(f"Status: {health['status']}")
print(f"Connection: {health['connection']}")
```

### Cleanup Operations
```python
# Clean up old logs
db_service.cleanup_old_logs(days=90)

# Get database statistics
stats = db_service.get_database_stats()
```

### Backup Strategy
- Automated daily backups
- Point-in-time recovery
- Cross-region replication (production)
- Backup verification

## 🧪 Testing

### Test Database Setup
```python
# Use separate test database
DATABASE_URL = "sqlite:///./test_agentic_ecom.db"

# Reset database between tests
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
```

### Test Data
```python
# Use factories for test data
from db.seeds.sample_data import create_sample_products

def test_product_creation():
    products = create_sample_products(db)
    assert len(products) > 0
```

## 📊 Monitoring

### Key Metrics
- Database connection health
- Query performance
- Table sizes
- Index usage
- Lock contention

### Alerts
- Connection failures
- Slow queries (>1s)
- Low disk space
- High error rates

## 🔧 Configuration

### Environment Variables
```bash
# Database URL
DATABASE_URL=sqlite:///./agentic_ecom.db

# Connection pool settings
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_TIMEOUT=30
```

### Configuration File
```yaml
# config/db_settings.yaml
database:
  connection:
    url: "sqlite:///./agentic_ecom.db"
    pool_size: 10
  development:
    echo_sql: true
    seed_sample_data: true
```

## 🚀 Production Deployment

### PostgreSQL Setup
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb agentic_ecom

# Update DATABASE_URL
DATABASE_URL=postgresql://user:password@localhost/agentic_ecom
```

### Performance Tuning
- Configure connection pooling
- Optimize PostgreSQL settings
- Set up read replicas
- Implement caching layer

### Security
- Enable SSL connections
- Use connection encryption
- Implement row-level security
- Regular security updates

## 📚 API Integration

### FastAPI Integration
```python
from fastapi import Depends
from db.database import get_db
from services.db_service import DatabaseService

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    db_service = DatabaseService(db)
    return db_service.get_products()
```

### Agent Integration
```python
# In your agents
from services.db_service import DatabaseService

class SalesGenie:
    def __init__(self, db: Session):
        self.db_service = DatabaseService(db)
    
    def create_product(self, product_data):
        return self.db_service.create_product(product_data)
```

## 🎯 Best Practices

### Data Integrity
- Use transactions for multi-table operations
- Implement proper foreign key constraints
- Validate data before insertion
- Use enums for status fields

### Performance
- Use appropriate indexes
- Implement pagination
- Cache frequently accessed data
- Monitor query performance

### Security
- Use parameterized queries
- Implement proper access controls
- Encrypt sensitive data
- Regular security audits

### Maintenance
- Regular backups
- Monitor database size
- Clean up old logs
- Update database software

## 🆘 Troubleshooting

### Common Issues

**Connection Errors**
```bash
# Check database URL
echo $DATABASE_URL

# Test connection
python db/init_database.py --action info
```

**Migration Issues**
```bash
# Reset database
python db/init_database.py --action reset

# Check migration status
alembic current
```

**Performance Issues**
```python
# Enable SQL logging
engine = create_engine(DATABASE_URL, echo=True)

# Check slow queries
# Monitor database statistics
```

## 📞 Support

For database-related issues:
1. Check the logs for error messages
2. Verify database connection settings
3. Test with the database management script
4. Review this documentation
5. Check SQLAlchemy and PostgreSQL documentation

---

**Database System Version**: 1.0.0  
**Last Updated**: December 2024  
**Compatible with**: SQLAlchemy 2.0+, PostgreSQL 12+, SQLite 3.35+ 