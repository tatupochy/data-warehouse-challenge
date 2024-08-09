#!/bin/bash
set -e

# Esperar a que PostgreSQL esté listo
while ! pg_isready -h postgres -p 5432 -U airflow; do
  echo "Esperando a que PostgreSQL esté listo..."
  sleep 2
done

# Ejecutar comandos SQL para crear tablas
psql -h postgres -U airflow -d airflow <<EOF
-- Crear la tabla de hechos fact_sales
CREATE TABLE IF NOT EXISTS fact_sales (
    sale_id SERIAL PRIMARY KEY,
    date_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    store_id INTEGER NOT NULL,
    sale_amount DECIMAL NOT NULL,
    quantity_sold INTEGER NOT NULL,
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (store_id) REFERENCES dim_store(store_id)
);

-- Crear la tabla de hechos fact_inventory
CREATE TABLE IF NOT EXISTS fact_inventory (
    inventory_id SERIAL PRIMARY KEY,
    date_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    store_id INTEGER NOT NULL,
    inventory_level INTEGER NOT NULL,
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY (store_id) REFERENCES dim_store(store_id)
);

-- Crear la tabla de hechos fact_customer_orders
CREATE TABLE IF NOT EXISTS fact_customer_orders (
    order_id SERIAL PRIMARY KEY,
    date_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    order_amount DECIMAL NOT NULL,
    items_ordered INTEGER NOT NULL,
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id)
);

-- Crear la tabla de hechos fact_store_performance
CREATE TABLE IF NOT EXISTS fact_store_performance (
    performance_id SERIAL PRIMARY KEY,
    date_id INTEGER NOT NULL,
    store_id INTEGER NOT NULL,
    total_sales DECIMAL NOT NULL,
    total_customers INTEGER NOT NULL,
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (store_id) REFERENCES dim_store(store_id)
);

-- Crear otras tablas dimension si es necesario
EOF

echo "Tablas de la base de datos creadas exitosamente."
