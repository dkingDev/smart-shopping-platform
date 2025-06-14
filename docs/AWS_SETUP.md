# AWS PostgreSQL Integration Guide

## 🎯 Perfect Setup for Your Morrisons Crawler + AWS PostgreSQL

Your workspace is now optimized for **national branded products price tracking** with AWS PostgreSQL backend.

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Copy environment template
copy config\.env.example config\.env

# Edit config\.env with your AWS RDS details:
# AWS_DB_HOST=your-rds-endpoint.amazonaws.com
# AWS_DB_PORT=5432
# AWS_DB_NAME=national_products
# AWS_DB_USER=your_username
# AWS_DB_PASSWORD=your_password
```

### 2. Install Dependencies
```bash
pip install psycopg2-binary pandas python-dotenv
```

### 3. Test & Setup Database
```bash
python setup_aws_database.py
```

### 4. Integrate Your Crawler
```bash
# Your Morrisons crawler goes in:
crawlers/morrisons/

# Use the integration template:
python crawlers/morrisons/morrisons_aws_integration.py
```

## 📊 What You Get

### ✅ **AWS PostgreSQL Database**
- **Optimized schema** for AWS RDS performance
- **Auto-scaling** and managed backups
- **SSL connections** for security
- **Connection pooling** for efficiency

### ✅ **Smart Data Processing**
- **Branded products only** (no store own-brands)
- **Price change tracking** with history
- **Duplicate prevention** across stores
- **Image validation** for brand verification

### ✅ **Multi-Store Ready**
- **8 UK retailers** pre-configured
- **Consistent product IDs** across stores
- **Efficient price updates** (only when changed)
- **Cross-store price comparison**

## 🏗️ Database Schema

```sql
-- Master products (3,710 branded items)
branded_products (product_id, name, brand, category, image_filename)

-- Store-specific pricing (updates frequently)  
store_prices (product_id, store_name, current_price, offer_text)

-- Price change history (analytics)
price_history_log (product_id, store_name, old_price, new_price, change_date)
```

## 🔄 Crawler Integration Pattern

```python
# Your existing crawler flow:
1. Scrape Morrisons → Raw Data
2. Filter branded products → Validated Data  
3. Update AWS PostgreSQL → Store Prices
4. Generate analytics → Price Comparisons
```

## 💡 Key Benefits

🎯 **No Docker Required**: Direct AWS PostgreSQL connection  
⚡ **Efficient Updates**: Only price changes, not full catalog  
🔍 **Brand Focus**: 3,710 verified branded products only  
📈 **Analytics Ready**: Price history and trend analysis  
🌍 **National Scale**: Ready for all UK supermarkets  

## 🛠️ File Structure

```
crawlers/morrisons/           # Your crawler here
├── your_crawler.py          # Your existing crawler
└── morrisons_aws_integration.py  # AWS integration

database/
├── aws_postgresql_schema.sql     # Database schema
├── aws_postgresql_manager.py     # Database manager
└── imports/master_branded_products.csv  # Product catalog

config/
├── master_config.json       # Main configuration
├── morrisons_config.json    # Store-specific config
└── .env                     # AWS credentials
```

## 🎯 Next Steps

1. **✅ Drop your Morrisons crawler** into `crawlers/morrisons/`
2. **✅ Configure AWS credentials** in `config/.env`
3. **✅ Run setup script**: `python setup_aws_database.py`
4. **✅ Test integration**: Adapt `morrisons_aws_integration.py`
5. **🚀 Start crawling**: National price tracking live!

## 📈 Example Queries

```sql
-- Compare prices across stores
SELECT bp.name, bp.brand, sp.store_name, sp.current_price
FROM branded_products bp
JOIN store_prices sp ON bp.product_id = sp.product_id  
WHERE bp.brand = 'Dylon'
ORDER BY sp.current_price;

-- Track price changes
SELECT product_id, old_price, new_price, change_date
FROM price_history_log 
WHERE change_date > CURRENT_DATE - INTERVAL '7 days'
ORDER BY ABS(new_price - old_price) DESC;
```

**Your AWS PostgreSQL system is ready for national branded products price tracking! 🇬🇧🛒**
