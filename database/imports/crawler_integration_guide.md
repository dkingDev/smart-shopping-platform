# Multi-Retailer Crawler Integration Guide

## Database Design Philosophy

This system separates **BRANDED PRODUCT CATALOG** from **STORE-SPECIFIC DATA**:

### Master Branded Products Table
- **Product ID**: Consistent across all retailers
- **Normalized Name**: Brand + Product standardized
- **Brand**: Extracted brand name
- **Category**: Standardized category
- **Reference Data**: Image, base info

### Store-Specific Pricing Table
- **Store Name**: "Morrisons", "Tesco", "ASDA", etc.
- **Current Price**: Store's current price
- **Availability**: In stock / out of stock
- **Offer Text**: Store-specific promotions
- **Last Updated**: Timestamp for freshness

## Crawler Implementation Strategy

### 1. Initial Setup
```sql
-- Load master branded products (one-time)
LOAD DATA INFILE 'master_branded_products.csv' 
INTO TABLE branded_products;
```

### 2. Store Crawler Logic
```python
def update_store_prices(store_name, scraped_products):
    for product in scraped_products:
        # Match to master product by name similarity
        product_id = find_matching_product_id(product.name)
        
        if product_id:
            # Update existing store price
            upsert_store_price(product_id, store_name, product.price, product.offer)
        else:
            # New branded product discovered
            if is_branded_product(product):
                # Add to master catalog
                new_product_id = add_to_master_catalog(product)
                # Add store price
                add_store_price(new_product_id, store_name, product.price)
```

### 3. Price Update Strategy
```python
def intelligent_price_update(product_id, store_name, new_price, new_offer):
    current = get_current_store_price(product_id, store_name)
    
    # Only update if price changed or offer changed
    if current.price != new_price or current.offer != new_offer:
        update_store_price(product_id, store_name, new_price, new_offer)
        log_price_change(product_id, store_name, current.price, new_price)
```

## Benefits for Multi-Retailer System

1. **Avoid Duplicate Products**: Same branded product across stores shares product_id
2. **Price Comparison**: Easy to compare prices across retailers
3. **Efficient Updates**: Only update when prices actually change
4. **Brand Consistency**: Normalized brand names across all stores
5. **Flexible Schema**: Easy to add new retailers without changing structure

## Example Queries

### Compare Prices Across Stores
```sql
SELECT bp.name, bp.brand, sp.store_name, sp.current_price, sp.offer_text
FROM branded_products bp
JOIN store_prices sp ON bp.product_id = sp.product_id
WHERE bp.brand = 'Dylon'
ORDER BY bp.name, sp.current_price;
```

### Find New Products by Store
```sql
SELECT bp.name, bp.brand, sp.current_price
FROM branded_products bp
JOIN store_prices sp ON bp.product_id = sp.product_id
WHERE sp.store_name = 'Tesco' 
AND bp.data_source = 'morrisons_branded_catalog'
AND sp.last_updated > '2025-06-01';
```

### Track Price Changes
```sql
SELECT product_id, store_name, current_price, last_updated
FROM store_prices 
WHERE last_updated > DATE_SUB(NOW(), INTERVAL 7 DAY)
ORDER BY last_updated DESC;
```

This design allows your crawler to efficiently update only changed prices while maintaining a clean master catalog of branded products!
