-- Master Branded Products Database Schema
-- For multi-retailer product database system

-- Main products table
CREATE TABLE branded_products (
    product_id VARCHAR(12) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    original_name VARCHAR(255),
    brand VARCHAR(100),
    category VARCHAR(100),
    category_id VARCHAR(50),
    image_filename VARCHAR(255),
    reference_price DECIMAL(10,2),
    has_offer BOOLEAN DEFAULT FALSE,
    created_date DATE,
    data_source VARCHAR(50),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Store-specific pricing table (separate from master products)
CREATE TABLE store_prices (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(12) REFERENCES branded_products(product_id),
    store_name VARCHAR(100) NOT NULL,
    current_price DECIMAL(10,2),
    offer_text TEXT,
    availability BOOLEAN DEFAULT TRUE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(product_id, store_name)
);

-- Categories reference
CREATE TABLE categories (
    category_id VARCHAR(50) PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    product_count INTEGER DEFAULT 0
);

-- Brands catalog
CREATE TABLE brands (
    brand_name VARCHAR(100) PRIMARY KEY,
    product_count INTEGER DEFAULT 0,
    min_price DECIMAL(10,2),
    max_price DECIMAL(10,2)
);

-- Indexes for performance
CREATE INDEX idx_branded_products_brand ON branded_products(brand);
CREATE INDEX idx_branded_products_category ON branded_products(category_id);
CREATE INDEX idx_store_prices_store ON store_prices(store_name);
CREATE INDEX idx_store_prices_updated ON store_prices(last_updated);
