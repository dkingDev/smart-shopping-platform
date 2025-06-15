-- AWS PostgreSQL Setup for National Branded Products System
-- Optimized for AWS RDS PostgreSQL with performance considerations

-- Enable extensions for better performance
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Users table for authentication system
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_premium BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    subscription_type VARCHAR(50) DEFAULT 'free' -- 'free', 'premium', 'business'
);

-- User shopping lists
CREATE TABLE shopping_lists (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    is_shared BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_shopping_lists_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Shopping list items (triggers crawler priorities)
CREATE TABLE shopping_list_items (
    id SERIAL PRIMARY KEY,
    list_id INTEGER NOT NULL,
    product_id VARCHAR(12),
    product_name VARCHAR(255) NOT NULL,
    quantity INTEGER DEFAULT 1,
    notes TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    preferred_stores TEXT[], -- Array of store names
    price_alert_threshold DECIMAL(10,2),
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_list_items_list FOREIGN KEY (list_id) REFERENCES shopping_lists(id) ON DELETE CASCADE,
    CONSTRAINT fk_list_items_product FOREIGN KEY (product_id) REFERENCES branded_products(product_id) ON DELETE SET NULL
);

-- User crawler priorities (generated from shopping lists and searches)
CREATE TABLE user_crawler_priorities (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product_search VARCHAR(255) NOT NULL,
    store_name VARCHAR(100),
    priority_score INTEGER DEFAULT 1,
    source VARCHAR(50) NOT NULL, -- 'shopping_list', 'search', 'product_view'
    last_crawled TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_crawler_priorities_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- User activity tracking for business intelligence
CREATE TABLE user_activity (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    action_type VARCHAR(50) NOT NULL, -- 'search', 'product_view', 'list_add', 'store_browse'
    action_data JSONB, -- Flexible data storage
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_activity_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Store promotions and sponsored content management
CREATE TABLE store_promotions (
    id SERIAL PRIMARY KEY,
    store_name VARCHAR(100) NOT NULL,
    promotion_type VARCHAR(50) NOT NULL, -- 'sponsored_banner', 'product_highlight', 'category_feature'
    title VARCHAR(255) NOT NULL,
    description TEXT,
    image_url VARCHAR(500),
    target_url VARCHAR(500),
    promotion_data JSONB, -- Flexible promo data (discount %, categories, etc.)
    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_date TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    display_priority INTEGER DEFAULT 1,
    max_impressions INTEGER,
    current_impressions INTEGER DEFAULT 0,
    cost_per_impression DECIMAL(10,4),
    revenue_generated DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User location preferences for store availability
CREATE TABLE user_locations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    location_name VARCHAR(255) NOT NULL, -- e.g., "Home", "Work", "Main"
    postcode VARCHAR(10),
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    is_primary BOOLEAN DEFAULT FALSE,
    available_stores TEXT[], -- Array of store names available in this location
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_locations_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Shopping list templates and smart switching history
CREATE TABLE shopping_list_templates (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    template_name VARCHAR(255) NOT NULL,
    base_items JSONB NOT NULL, -- Standard items for this template
    frequency VARCHAR(50), -- 'weekly', 'monthly', 'custom'
    auto_create BOOLEAN DEFAULT FALSE,
    last_used TIMESTAMP,
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_list_templates_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Store switching history and smart recommendations
CREATE TABLE store_switch_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    original_list_id INTEGER NOT NULL,
    original_store VARCHAR(100) NOT NULL,
    target_store VARCHAR(100) NOT NULL,
    switch_type VARCHAR(50) NOT NULL, -- 'smart_auto', 'manual_override', 'location_based'
    items_switched INTEGER DEFAULT 0,
    items_unavailable INTEGER DEFAULT 0,
    estimated_savings DECIMAL(10,2),
    actual_savings DECIMAL(10,2),
    user_satisfaction_rating INTEGER, -- 1-5 rating
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_store_switch_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_store_switch_list FOREIGN KEY (original_list_id) REFERENCES shopping_lists(id) ON DELETE CASCADE
);

-- Product availability by store and location
CREATE TABLE product_availability (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(12) NOT NULL,
    store_name VARCHAR(100) NOT NULL,
    location_identifier VARCHAR(100), -- postcode, city, or region
    is_available BOOLEAN DEFAULT TRUE,
    stock_level VARCHAR(50), -- 'in_stock', 'low_stock', 'out_of_stock'
    delivery_available BOOLEAN DEFAULT TRUE,
    click_collect_available BOOLEAN DEFAULT TRUE,
    last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_product_store_location UNIQUE (product_id, store_name, location_identifier),
    CONSTRAINT fk_product_availability_product FOREIGN KEY (product_id) REFERENCES branded_products(product_id) ON DELETE CASCADE
);

-- Cost savings analysis and recommendations
CREATE TABLE savings_analysis (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    analysis_type VARCHAR(50) NOT NULL, -- 'list_comparison', 'store_switch', 'bulk_discount'
    comparison_data JSONB NOT NULL, -- Store prices, quantities, offers
    potential_savings DECIMAL(10,2) NOT NULL,
    recommended_action TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    was_acted_upon BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_savings_analysis_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Main branded products table (master catalog)
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
    created_date DATE DEFAULT CURRENT_DATE,
    data_source VARCHAR(50) DEFAULT 'crawler',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- AWS RDS optimizations
    search_vector tsvector -- For full-text search
);

-- Store-specific pricing table (frequent updates)
CREATE TABLE store_prices (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(12) NOT NULL,
    store_name VARCHAR(100) NOT NULL,
    current_price DECIMAL(10,2) NOT NULL,
    previous_price DECIMAL(10,2),
    offer_text TEXT,
    availability BOOLEAN DEFAULT TRUE,
    price_change_date DATE DEFAULT CURRENT_DATE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Prevent duplicate store/product combinations
    CONSTRAINT unique_store_product UNIQUE (product_id, store_name)
);

-- Price history log for tracking changes
CREATE TABLE price_history_log (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(12) NOT NULL,
    store_name VARCHAR(100) NOT NULL,
    old_price DECIMAL(10,2),
    new_price DECIMAL(10,2),
    price_change DECIMAL(10,2) GENERATED ALWAYS AS (new_price - old_price) STORED,
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    change_reason VARCHAR(50) -- 'crawl_update', 'manual_correction', etc.
);

-- Categories reference table
CREATE TABLE product_categories (
    category_id VARCHAR(50) PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    product_count INTEGER DEFAULT 0,
    avg_price DECIMAL(10,2),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Brands catalog table
CREATE TABLE brand_catalog (
    brand_name VARCHAR(100) PRIMARY KEY,
    product_count INTEGER DEFAULT 0,
    min_price DECIMAL(10,2),
    max_price DECIMAL(10,2),
    avg_price DECIMAL(10,2),
    categories_count INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AWS RDS Performance Indexes
-- User authentication indexes
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_active ON users(is_active);

-- Shopping lists indexes
CREATE INDEX idx_shopping_lists_user ON shopping_lists(user_id);
CREATE INDEX idx_shopping_lists_updated ON shopping_lists(updated_at);

-- Shopping list items indexes
CREATE INDEX idx_list_items_list ON shopping_list_items(list_id);
CREATE INDEX idx_list_items_product ON shopping_list_items(product_id);
CREATE INDEX idx_list_items_completed ON shopping_list_items(is_completed);

-- Crawler priorities indexes
CREATE INDEX idx_crawler_priorities_user ON user_crawler_priorities(user_id);
CREATE INDEX idx_crawler_priorities_score ON user_crawler_priorities(priority_score DESC);
CREATE INDEX idx_crawler_priorities_store ON user_crawler_priorities(store_name);
CREATE INDEX idx_crawler_priorities_last_crawled ON user_crawler_priorities(last_crawled NULLS FIRST);

-- User activity indexes for analytics
CREATE INDEX idx_user_activity_user ON user_activity(user_id);
CREATE INDEX idx_user_activity_type ON user_activity(action_type);
CREATE INDEX idx_user_activity_created ON user_activity(created_at);

-- Store promotions indexes
CREATE INDEX idx_store_promotions_active ON store_promotions(is_active, display_priority);
CREATE INDEX idx_store_promotions_store ON store_promotions(store_name);
CREATE INDEX idx_store_promotions_type ON store_promotions(promotion_type);
CREATE INDEX idx_store_promotions_dates ON store_promotions(start_date, end_date);

-- User locations indexes
CREATE INDEX idx_user_locations_user ON user_locations(user_id);
CREATE INDEX idx_user_locations_primary ON user_locations(is_primary);
CREATE INDEX idx_user_locations_postcode ON user_locations(postcode);

-- Shopping list templates indexes
CREATE INDEX idx_list_templates_user ON shopping_list_templates(user_id);
CREATE INDEX idx_list_templates_frequency ON shopping_list_templates(frequency);
CREATE INDEX idx_list_templates_auto ON shopping_list_templates(auto_create);

-- Store switch history indexes
CREATE INDEX idx_store_switch_user ON store_switch_history(user_id);
CREATE INDEX idx_store_switch_stores ON store_switch_history(original_store, target_store);
CREATE INDEX idx_store_switch_type ON store_switch_history(switch_type);
CREATE INDEX idx_store_switch_savings ON store_switch_history(estimated_savings DESC);

-- Product availability indexes
CREATE INDEX idx_product_availability_product ON product_availability(product_id);
CREATE INDEX idx_product_availability_store ON product_availability(store_name);
CREATE INDEX idx_product_availability_location ON product_availability(location_identifier);
CREATE INDEX idx_product_availability_stock ON product_availability(is_available, stock_level);

-- Savings analysis indexes
CREATE INDEX idx_savings_analysis_user ON savings_analysis(user_id);
CREATE INDEX idx_savings_analysis_type ON savings_analysis(analysis_type);
CREATE INDEX idx_savings_analysis_savings ON savings_analysis(potential_savings DESC);
CREATE INDEX idx_savings_analysis_expires ON savings_analysis(expires_at);

-- Primary lookup indexes
CREATE INDEX idx_branded_products_brand ON branded_products(brand);
CREATE INDEX idx_branded_products_category ON branded_products(category_id);
CREATE INDEX idx_branded_products_name_search ON branded_products USING gin(search_vector);

-- Store prices indexes for fast lookups
CREATE INDEX idx_store_prices_store ON store_prices(store_name);
CREATE INDEX idx_store_prices_product ON store_prices(product_id);
CREATE INDEX idx_store_prices_updated ON store_prices(last_updated);
CREATE INDEX idx_store_prices_price ON store_prices(current_price);

-- Price history indexes for analytics
CREATE INDEX idx_price_history_product_date ON price_history_log(product_id, change_date);
CREATE INDEX idx_price_history_store_date ON price_history_log(store_name, change_date);

-- Foreign key constraints
ALTER TABLE store_prices 
ADD CONSTRAINT fk_store_prices_product 
FOREIGN KEY (product_id) REFERENCES branded_products(product_id) 
ON DELETE CASCADE;

ALTER TABLE price_history_log 
ADD CONSTRAINT fk_price_history_product 
FOREIGN KEY (product_id) REFERENCES branded_products(product_id) 
ON DELETE CASCADE;

-- Triggers for maintaining data consistency
-- Update search vector when product name changes
CREATE OR REPLACE FUNCTION update_search_vector() RETURNS trigger AS $$
BEGIN
    NEW.search_vector := to_tsvector('english', NEW.name || ' ' || COALESCE(NEW.brand, ''));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER branded_products_search_update
    BEFORE INSERT OR UPDATE ON branded_products
    FOR EACH ROW EXECUTE FUNCTION update_search_vector();

-- Log price changes automatically
CREATE OR REPLACE FUNCTION log_price_change() RETURNS trigger AS $$
BEGIN
    -- Only log if price actually changed
    IF OLD.current_price IS DISTINCT FROM NEW.current_price THEN
        INSERT INTO price_history_log (product_id, store_name, old_price, new_price, change_reason)
        VALUES (NEW.product_id, NEW.store_name, OLD.current_price, NEW.current_price, 'crawl_update');
        
        -- Update previous_price
        NEW.previous_price := OLD.current_price;
        NEW.price_change_date := CURRENT_DATE;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER store_prices_change_log
    BEFORE UPDATE ON store_prices
    FOR EACH ROW EXECUTE FUNCTION log_price_change();

-- Trigger to update shopping list timestamp when items change
CREATE OR REPLACE FUNCTION update_shopping_list_timestamp() RETURNS trigger AS $$
BEGIN
    UPDATE shopping_lists 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE id = COALESCE(NEW.list_id, OLD.list_id);
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER shopping_list_items_update
    AFTER INSERT OR UPDATE OR DELETE ON shopping_list_items
    FOR EACH ROW EXECUTE FUNCTION update_shopping_list_timestamp();

-- Trigger to create crawler priorities from shopping list items
CREATE OR REPLACE FUNCTION create_crawler_priority_from_list() RETURNS trigger AS $$
BEGIN
    -- Get the user_id from the shopping list
    INSERT INTO user_crawler_priorities (user_id, product_search, store_name, priority_score, source)
    SELECT 
        sl.user_id,
        NEW.product_name,
        unnest(COALESCE(NEW.preferred_stores, ARRAY['all_stores'])),
        3, -- High priority for shopping list items
        'shopping_list'
    FROM shopping_lists sl
    WHERE sl.id = NEW.list_id
    ON CONFLICT DO NOTHING; -- Avoid duplicates
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER list_items_create_priority
    AFTER INSERT ON shopping_list_items
    FOR EACH ROW EXECUTE FUNCTION create_crawler_priority_from_list();

-- Functions for maintaining statistics
CREATE OR REPLACE FUNCTION update_category_stats() RETURNS void AS $$
BEGIN
    UPDATE product_categories SET
        product_count = counts.count,
        last_updated = CURRENT_TIMESTAMP
    FROM (
        SELECT category_id, COUNT(*) as count
        FROM branded_products
        GROUP BY category_id
    ) AS counts
    WHERE product_categories.category_id = counts.category_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_brand_stats() RETURNS void AS $$
BEGIN
    UPDATE brand_catalog SET
        product_count = stats.count,
        min_price = stats.min_price,
        max_price = stats.max_price,
        avg_price = stats.avg_price,
        last_updated = CURRENT_TIMESTAMP
    FROM (
        SELECT 
            bp.brand,
            COUNT(*) as count,
            MIN(sp.current_price) as min_price,
            MAX(sp.current_price) as max_price,
            ROUND(AVG(sp.current_price), 2) as avg_price
        FROM branded_products bp
        LEFT JOIN store_prices sp ON bp.product_id = sp.product_id
        WHERE bp.brand IS NOT NULL
        GROUP BY bp.brand
    ) AS stats
    WHERE brand_catalog.brand_name = stats.brand;
END;
$$ LANGUAGE plpgsql;

-- Function to get top crawler priorities for scheduling
CREATE OR REPLACE FUNCTION get_top_crawler_priorities(limit_count INTEGER DEFAULT 100) RETURNS TABLE(
    product_search VARCHAR,
    store_name VARCHAR,
    total_priority_score BIGINT,
    user_count BIGINT,
    last_crawled TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ucp.product_search,
        ucp.store_name,
        SUM(ucp.priority_score) as total_priority_score,
        COUNT(DISTINCT ucp.user_id) as user_count,
        MAX(ucp.last_crawled) as last_crawled
    FROM user_crawler_priorities ucp
    WHERE ucp.last_crawled IS NULL 
       OR ucp.last_crawled < CURRENT_TIMESTAMP - INTERVAL '24 hours'
    GROUP BY ucp.product_search, ucp.store_name
    ORDER BY total_priority_score DESC, user_count DESC
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql;

-- Function to mark crawler priorities as completed
CREATE OR REPLACE FUNCTION mark_crawler_priority_completed(
    search_term VARCHAR,
    store VARCHAR
) RETURNS void AS $$
BEGIN
    UPDATE user_crawler_priorities 
    SET last_crawled = CURRENT_TIMESTAMP
    WHERE product_search = search_term 
      AND store_name = store;
END;
$$ LANGUAGE plpgsql;

-- Function to analyze potential savings before creating shopping list
CREATE OR REPLACE FUNCTION analyze_shopping_list_savings(
    user_id_param INTEGER,
    items JSONB,
    preferred_store VARCHAR DEFAULT NULL
) RETURNS TABLE(
    store_name VARCHAR,
    total_cost DECIMAL,
    potential_savings DECIMAL,
    unavailable_items INTEGER,
    best_offers TEXT[]
) AS $$
BEGIN
    RETURN QUERY
    WITH item_prices AS (
        SELECT 
            sp.store_name,
            jsonb_array_elements_text(items) as item_name,
            MIN(sp.current_price) as price,
            array_agg(sp.offer_text) FILTER (WHERE sp.offer_text IS NOT NULL) as offers
        FROM store_prices sp
        JOIN branded_products bp ON sp.product_id = bp.product_id
        WHERE bp.name ILIKE ANY(SELECT '%' || jsonb_array_elements_text(items) || '%')
        GROUP BY sp.store_name, jsonb_array_elements_text(items)
    ),
    store_totals AS (
        SELECT 
            ip.store_name,
            SUM(ip.price) as total_cost,
            COUNT(*) as available_items,
            array_agg(DISTINCT unnest(ip.offers)) FILTER (WHERE array_length(ip.offers, 1) > 0) as best_offers
        FROM item_prices ip
        GROUP BY ip.store_name
    )
    SELECT 
        st.store_name,
        st.total_cost,
        (SELECT MIN(total_cost) FROM store_totals) - st.total_cost as potential_savings,
        (jsonb_array_length(items) - st.available_items)::INTEGER as unavailable_items,
        COALESCE(st.best_offers, ARRAY[]::TEXT[]) as best_offers
    FROM store_totals st
    ORDER BY st.total_cost ASC;
END;
$$ LANGUAGE plpgsql;

-- Function to get smart store switching recommendations
CREATE OR REPLACE FUNCTION get_smart_store_switch_options(
    list_id_param INTEGER,
    user_location VARCHAR DEFAULT NULL
) RETURNS TABLE(
    target_store VARCHAR,
    switchable_items INTEGER,
    unavailable_items INTEGER,
    estimated_savings DECIMAL,
    availability_score DECIMAL,
    recommendation_score DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    WITH list_items AS (
        SELECT sli.product_name, sli.quantity, sli.product_id
        FROM shopping_list_items sli
        WHERE sli.list_id = list_id_param
    ),
    store_analysis AS (
        SELECT 
            sp.store_name,
            COUNT(CASE WHEN pa.is_available = true THEN 1 END) as available_items,
            COUNT(*) as total_items,
            SUM(sp.current_price * li.quantity) as total_cost,
            AVG(CASE WHEN pa.is_available = true THEN 1.0 ELSE 0.0 END) as availability_ratio
        FROM list_items li
        LEFT JOIN branded_products bp ON bp.name ILIKE '%' || li.product_name || '%'
        LEFT JOIN store_prices sp ON bp.product_id = sp.product_id
        LEFT JOIN product_availability pa ON bp.product_id = pa.product_id 
            AND sp.store_name = pa.store_name
            AND (user_location IS NULL OR pa.location_identifier = user_location)
        GROUP BY sp.store_name
    )
    SELECT 
        sa.store_name as target_store,
        sa.available_items::INTEGER as switchable_items,
        (sa.total_items - sa.available_items)::INTEGER as unavailable_items,
        (SELECT MIN(total_cost) FROM store_analysis) - sa.total_cost as estimated_savings,
        sa.availability_ratio as availability_score,
        -- Recommendation score: balance savings with availability
        (sa.availability_ratio * 0.6 + 
         CASE WHEN sa.total_cost > 0 THEN 
            (1.0 - (sa.total_cost / NULLIF((SELECT MAX(total_cost) FROM store_analysis), 0))) * 0.4 
         ELSE 0 END) as recommendation_score
    FROM store_analysis sa
    WHERE sa.total_cost IS NOT NULL
    ORDER BY recommendation_score DESC;
END;
$$ LANGUAGE plpgsql;

-- Function to get active store promotions for main page
CREATE OR REPLACE FUNCTION get_active_store_promotions(
    promotion_type_filter VARCHAR DEFAULT NULL,
    limit_count INTEGER DEFAULT 10
) RETURNS TABLE(
    id INTEGER,
    store_name VARCHAR,
    promotion_type VARCHAR,
    title VARCHAR,
    description TEXT,
    image_url VARCHAR,
    target_url VARCHAR,
    promotion_data JSONB,
    display_priority INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        sp.id,
        sp.store_name,
        sp.promotion_type,
        sp.title,
        sp.description,
        sp.image_url,
        sp.target_url,
        sp.promotion_data,
        sp.display_priority
    FROM store_promotions sp
    WHERE sp.is_active = true
      AND (sp.start_date IS NULL OR sp.start_date <= CURRENT_TIMESTAMP)
      AND (sp.end_date IS NULL OR sp.end_date >= CURRENT_TIMESTAMP)
      AND (sp.max_impressions IS NULL OR sp.current_impressions < sp.max_impressions)
      AND (promotion_type_filter IS NULL OR sp.promotion_type = promotion_type_filter)
    ORDER BY sp.display_priority DESC, sp.created_at DESC
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql;

-- Function to record promotion impression and track revenue
CREATE OR REPLACE FUNCTION record_promotion_impression(
    promotion_id_param INTEGER,
    user_id_param INTEGER DEFAULT NULL
) RETURNS void AS $$
BEGIN
    UPDATE store_promotions 
    SET 
        current_impressions = current_impressions + 1,
        revenue_generated = revenue_generated + cost_per_impression
    WHERE id = promotion_id_param;
    
    -- Log the impression for analytics
    INSERT INTO user_activity (user_id, action_type, action_data)
    VALUES (user_id_param, 'promotion_view', 
            jsonb_build_object('promotion_id', promotion_id_param, 'timestamp', CURRENT_TIMESTAMP));
END;
$$ LANGUAGE plpgsql;

-- Function to create shopping list from template with smart suggestions
CREATE OR REPLACE FUNCTION create_list_from_template(
    user_id_param INTEGER,
    template_id_param INTEGER,
    list_name VARCHAR,
    target_store VARCHAR DEFAULT NULL
) RETURNS INTEGER AS $$
DECLARE
    new_list_id INTEGER;
    template_items JSONB;
BEGIN
    -- Get template items
    SELECT base_items INTO template_items
    FROM shopping_list_templates
    WHERE id = template_id_param AND user_id = user_id_param;
    
    -- Create new shopping list
    INSERT INTO shopping_lists (user_id, name, description)
    VALUES (user_id_param, list_name, 'Created from template')
    RETURNING id INTO new_list_id;
    
    -- Add items from template
    INSERT INTO shopping_list_items (list_id, product_name, quantity, preferred_stores)
    SELECT 
        new_list_id,
        item->>'name',
        (item->>'quantity')::INTEGER,
        CASE 
            WHEN target_store IS NOT NULL THEN ARRAY[target_store]
            ELSE ARRAY(SELECT jsonb_array_elements_text(item->'preferred_stores'))
        END
    FROM jsonb_array_elements(template_items) as item;
    
    -- Update template usage
    UPDATE shopping_list_templates 
    SET usage_count = usage_count + 1, last_used = CURRENT_TIMESTAMP
    WHERE id = template_id_param;
    
    RETURN new_list_id;
END;
$$ LANGUAGE plpgsql;

-- AWS RDS specific optimizations
-- Vacuum and analyze schedule (AWS RDS will handle this, but good to document)
-- VACUUM ANALYZE branded_products;
-- VACUUM ANALYZE store_prices;

-- Create materialized view for fast price comparisons
CREATE MATERIALIZED VIEW store_price_comparison AS
SELECT 
    bp.product_id,
    bp.name,
    bp.brand,
    bp.category,
    json_object_agg(sp.store_name, 
        json_build_object(
            'price', sp.current_price,
            'offer', sp.offer_text,
            'updated', sp.last_updated
        )
    ) as store_prices,
    MIN(sp.current_price) as min_price,
    MAX(sp.current_price) as max_price,
    ROUND(AVG(sp.current_price), 2) as avg_price,
    COUNT(sp.store_name) as stores_available
FROM branded_products bp
LEFT JOIN store_prices sp ON bp.product_id = sp.product_id
WHERE sp.availability = true
GROUP BY bp.product_id, bp.name, bp.brand, bp.category;

-- Index for the materialized view
CREATE INDEX idx_price_comparison_brand ON store_price_comparison(brand);
CREATE INDEX idx_price_comparison_category ON store_price_comparison(category);
CREATE INDEX idx_price_comparison_min_price ON store_price_comparison(min_price);

-- Function to refresh the materialized view (call after bulk updates)
CREATE OR REPLACE FUNCTION refresh_price_comparison() RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY store_price_comparison;
END;
$$ LANGUAGE plpgsql;

-- Grant permissions for application user
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user;

-- Performance monitoring queries (for AWS CloudWatch)
/*
-- Top products by price changes
SELECT product_id, COUNT(*) as change_count
FROM price_history_log 
WHERE change_date > CURRENT_DATE - INTERVAL '7 days'
GROUP BY product_id 
ORDER BY change_count DESC 
LIMIT 10;

-- Store update frequency
SELECT store_name, COUNT(*) as updates, MAX(last_updated) as last_update
FROM store_prices 
GROUP BY store_name 
ORDER BY updates DESC;

-- Database size monitoring
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
*/
