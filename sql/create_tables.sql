-- Crear la tabla de hechos fact_sales
CREATE TABLE IF NOT EXISTS fact_sales (
    sale_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    product_name VARCHAR NOT NULL,
    customer_name VARCHAR NOT NULL,
    store_name VARCHAR NOT NULL,
    sale_amount DECIMAL NOT NULL,
    quantity_sold INTEGER NOT NULL
);

-- Crear la tabla de hechos fact_inventory
CREATE TABLE IF NOT EXISTS fact_inventory (
    inventory_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    product_name VARCHAR NOT NULL,
    store_name VARCHAR NOT NULL,
    inventory_level INTEGER NOT NULL
);

-- Crear la tabla de hechos fact_customer_orders
CREATE TABLE IF NOT EXISTS fact_customer_orders (
    order_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    customer_name VARCHAR NOT NULL,
    order_amount DECIMAL NOT NULL,
    items_ordered INTEGER NOT NULL
);

-- Crear la tabla de hechos fact_store_performance
CREATE TABLE IF NOT EXISTS fact_store_performance (
    performance_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    store_name VARCHAR NOT NULL,
    total_sales DECIMAL NOT NULL,
    total_customers INTEGER NOT NULL
);
