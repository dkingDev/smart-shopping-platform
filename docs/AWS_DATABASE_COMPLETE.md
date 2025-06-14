# AWS Database Integration - Complete System

## Overview

You now have a comprehensive AWS PostgreSQL database system that powers the entire smart shopping platform. This includes:

- **Product & Price Database**: Universal product catalog with multi-store pricing
- **User Authentication**: JWT-based user system with registration/login
- **Shopping Lists**: Personalized lists that drive crawler priorities
- **Crawler Optimization**: User-driven data collection priorities
- **Business Intelligence**: Activity tracking and analytics

## Database Architecture

### Core Tables

1. **`branded_products`** - Master product catalog
   - Universal product IDs, names, brands, categories
   - Reference pricing and metadata
   - Full-text search capabilities

2. **`store_prices`** - Current pricing per store
   - Real-time price updates from crawlers
   - Availability and offer information
   - Automatic price change logging

3. **`price_history_log`** - Price change tracking
   - Historical price movements
   - Change detection and analytics
   - Trend analysis capabilities

### User System Tables

4. **`users`** - User authentication and profiles
   - Username, email, password management
   - Premium subscriptions and account types
   - Activity tracking

5. **`shopping_lists`** - User shopping lists
   - Named lists with descriptions
   - Sharing capabilities
   - Update tracking

6. **`shopping_list_items`** - Items in shopping lists
   - Product references and quantities
   - Preferred stores and price alerts
   - Completion tracking

### Intelligence Tables

7. **`user_crawler_priorities`** - Dynamic crawler scheduling
   - User-driven product search priorities
   - Store-specific crawling requests
   - Priority scoring and scheduling

8. **`user_activity`** - Business intelligence
   - Search patterns and product views
   - Shopping behavior analytics
   - Monetization insights

## Key Features

### Automatic Crawler Prioritization

When users add items to shopping lists, the system automatically:
- Creates high-priority crawler tasks
- Targets specific stores they prefer
- Updates prices for products they care about
- Optimizes crawler efficiency based on real user demand

### Smart Price Monitoring

- Automatic price change detection
- Historical price tracking
- Price alert thresholds per user
- Multi-store price comparison views

### Performance Optimizations

- AWS RDS-specific indexes and configurations
- Materialized views for fast price comparisons
- Batch operations for bulk updates
- Automatic statistics maintenance

## Environment Configuration

### Required Environment Variables

```bash
# AWS RDS PostgreSQL Connection
AWS_DB_HOST=your-rds-endpoint.amazonaws.com
AWS_DB_PORT=5432
AWS_DB_NAME=your_database_name
AWS_DB_USER=your_username
AWS_DB_PASSWORD=your_password

# JWT Authentication
JWT_SECRET_KEY=your-super-secret-jwt-key

# Optional
AWS_REGION=us-east-1
DEBUG=true
```

## Setup Process

### 1. Create AWS RDS Instance

```bash
# Create PostgreSQL RDS instance (via AWS Console or CLI)
aws rds create-db-instance \
  --db-instance-identifier smartshopping-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password your_password \
  --allocated-storage 20 \
  --vpc-security-group-ids sg-12345678
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your AWS RDS details
# Update AWS_DB_HOST, AWS_DB_USER, AWS_DB_PASSWORD, etc.
```

### 3. Initialize Database

```bash
# Install dependencies
pip install psycopg2-binary pandas python-dotenv

# Run setup script
python setup_aws_database.py

# Or setup manually
python database/aws_postgresql_manager.py
```

### 4. Test Integration

```bash
# Test FastAPI app with AWS database
python shopping_website_fastapi.py

# Run demo with real AWS integration
python demo_auth_shopping.py
```

## Database Functions Available

### User Management
- `create_user()` - Register new users
- `get_user_by_username()` - Authentication lookup
- `get_user_shopping_stats()` - User analytics

### Shopping Lists
- `create_shopping_list()` - Create personalized lists
- `add_to_shopping_list()` - Add items (triggers crawler priorities)
- Auto-updating timestamps and priority creation

### Crawler Intelligence
- `get_top_crawler_priorities()` - Get next products to crawl
- `mark_crawler_priority_completed()` - Update crawl status
- Automatic priority scoring based on user demand

### Price Management
- `upsert_store_prices()` - Update store pricing
- `get_price_comparison()` - Multi-store price views
- `refresh_price_comparison()` - Update materialized views

## Business Value

### Immediate Monetization
1. **User subscriptions** ($5-15/month for premium features)
2. **Affiliate revenue** (3-8% commission on purchases)
3. **B2B data licensing** ($500-5000/month for price data)
4. **Targeted advertising** (store promotions and product ads)

### Data Collection Value
- **User shopping patterns** drive crawler priorities
- **Real demand signals** optimize infrastructure costs
- **Price sensitivity data** enables dynamic pricing insights
- **Store preference analytics** for partnership opportunities

### Scalability Features
- AWS RDS auto-scaling capabilities
- Materialized views for performance
- Batch operations for efficiency
- Index optimization for fast queries

## Integration Points

### With FastAPI Website
```python
# User authentication
user = db.get_user_by_username(username)

# Shopping list management
list_id = db.create_shopping_list(user_id, "Weekly Groceries")
db.add_to_shopping_list(list_id, "Coca Cola", preferred_stores=["tesco", "morrisons"])
```

### With Universal Crawler
```python
# Get prioritized crawl targets
priorities = db.get_crawler_priorities(limit=50)

for priority in priorities:
    # Crawl priority.product_search at priority.store_name
    # Update prices via db.upsert_store_prices()
    # Mark complete via db.mark_priority_crawled()
```

### With Analytics
```python
# Business intelligence
stats = db.get_database_stats()
user_stats = db.get_user_shopping_stats(user_id)

# Track user activity
activity = {
    "search_term": "coca cola",
    "store": "tesco",
    "results_count": 12
}
# Store in user_activity table for BI
```

## Security Considerations

- **SSL/TLS encryption** for all database connections
- **Password hashing** using bcrypt or similar
- **JWT token security** with proper secret rotation
- **SQL injection prevention** via parameterized queries
- **AWS security groups** limiting database access

## Monitoring and Maintenance

### Performance Monitoring
```sql
-- Monitor table sizes
SELECT tablename, pg_size_pretty(pg_total_relation_size(tablename))
FROM pg_tables WHERE schemaname = 'public';

-- Check crawler priorities
SELECT COUNT(*) FROM user_crawler_priorities WHERE last_crawled IS NULL;

-- Price update frequency
SELECT store_name, COUNT(*), MAX(last_updated)
FROM store_prices GROUP BY store_name;
```

### Automated Maintenance
- Daily `VACUUM ANALYZE` for optimal performance
- Weekly materialized view refresh
- Monthly statistics updates
- Automatic price history archival

## Production Deployment

### AWS RDS Configuration
- **Multi-AZ deployment** for high availability
- **Read replicas** for analytics workloads  
- **Automated backups** with point-in-time recovery
- **Parameter group optimization** for PostgreSQL

### Scaling Strategy
- **Connection pooling** (pgbouncer)
- **Read/write splitting** for heavy analytics
- **Partitioning** for large price history tables
- **Caching layer** (Redis) for frequent queries

## Next Steps

1. **Deploy to Production**
   - Set up AWS RDS instance
   - Configure security groups and VPC
   - Deploy FastAPI app to Railway/Vercel

2. **Connect Live Data**
   - Integrate real store APIs
   - Deploy universal crawler
   - Set up price update schedules

3. **Enable Monetization**
   - Add affiliate tracking
   - Implement subscription billing
   - Set up B2B API access
   - Launch targeted advertising

4. **Scale and Optimize**
   - Monitor performance metrics
   - Optimize slow queries
   - Add caching layers
   - Implement data archival

Your AWS database is now ready to power a complete smart shopping platform with user-driven crawler optimization and immediate monetization capabilities!
