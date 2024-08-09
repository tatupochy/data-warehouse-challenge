from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pandas as pd
import psycopg2
import os

# Define the base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Load the environment variables
load_dotenv(os.path.join(BASE_DIR, '.env'))

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'etl_dag_fact_tables_only',
    default_args=default_args,
    description='ETL DAG to extract, transform, and load data into fact tables in PostgreSQL',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
)

# Define the extract, transform, and load functions
def extract_sales(**kwargs):
    file_path = os.path.join(BASE_DIR, 'dags', 'data', 'sales_data.csv')
    df = pd.read_csv(file_path)
    kwargs['ti'].xcom_push(key='sales_data', value=df.to_dict('records'))

def extract_inventory(**kwargs):
    file_path = os.path.join(BASE_DIR, 'dags', 'data', 'inventory_data.csv')
    df = pd.read_csv(file_path)
    kwargs['ti'].xcom_push(key='inventory_data', value=df.to_dict('records'))

def extract_customer_orders(**kwargs):
    file_path = os.path.join(BASE_DIR, 'dags', 'data', 'customer_orders_data.csv')
    df = pd.read_csv(file_path)
    kwargs['ti'].xcom_push(key='customer_orders_data', value=df.to_dict('records'))

def extract_store_performance(**kwargs):
    file_path = os.path.join(BASE_DIR, 'dags', 'data', 'store_performance_data.csv')
    df = pd.read_csv(file_path)
    kwargs['ti'].xcom_push(key='store_performance_data', value=df.to_dict('records'))

def transform_sales(**kwargs):
    data = kwargs['ti'].xcom_pull(key='sales_data', task_ids='extract_sales')
    df = pd.DataFrame(data)
    df['sale_amount'] = df['quantity_sold'] * df['price_per_unit']
    kwargs['ti'].xcom_push(key='transformed_sales_data', value=df.to_dict('records'))

def transform_inventory(**kwargs):
    data = kwargs['ti'].xcom_pull(key='inventory_data', task_ids='extract_inventory')
    df = pd.DataFrame(data)
    kwargs['ti'].xcom_push(key='transformed_inventory_data', value=df.to_dict('records'))

def transform_customer_orders(**kwargs):
    data = kwargs['ti'].xcom_pull(key='customer_orders_data', task_ids='extract_customer_orders')
    df = pd.DataFrame(data)
    df['order_amount'] = df['items_ordered'] * df['price_per_item']
    kwargs['ti'].xcom_push(key='transformed_customer_orders_data', value=df.to_dict('records'))

def transform_store_performance(**kwargs):
    data = kwargs['ti'].xcom_pull(key='store_performance_data', task_ids='extract_store_performance')
    df = pd.DataFrame(data)
    kwargs['ti'].xcom_push(key='transformed_store_performance_data', value=df.to_dict('records'))

def load_sales(**kwargs):
    data = kwargs['ti'].xcom_pull(key='transformed_sales_data', task_ids='transform_sales')
    df = pd.DataFrame(data)

    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    cur = conn.cursor()
    for index, row in df.iterrows():
        cur.execute(
            """
            INSERT INTO fact_sales (date, product_name, customer_name, store_name, sale_amount, quantity_sold)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (row['date'], row['product_name'], row['customer_name'], row['store_name'], row['sale_amount'], row['quantity_sold'])
        )
    conn.commit()
    cur.close()
    conn.close()

def load_inventory(**kwargs):
    data = kwargs['ti'].xcom_pull(key='transformed_inventory_data', task_ids='transform_inventory')
    df = pd.DataFrame(data)

    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    cur = conn.cursor()
    for index, row in df.iterrows():
        cur.execute(
            """
            INSERT INTO fact_inventory (date, product_name, store_name, inventory_level)
            VALUES (%s, %s, %s, %s)
            """,
            (row['date'], row['product_name'], row['store_name'], row['inventory_level'])
        )
    conn.commit()
    cur.close()
    conn.close()

def load_customer_orders(**kwargs):
    data = kwargs['ti'].xcom_pull(key='transformed_customer_orders_data', task_ids='transform_customer_orders')
    df = pd.DataFrame(data)

    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    cur = conn.cursor()
    for index, row in df.iterrows():
        cur.execute(
            """
            INSERT INTO fact_customer_orders (date, customer_name, order_amount, items_ordered)
            VALUES (%s, %s, %s, %s)
            """,
            (row['date'], row['customer_name'], row['order_amount'], row['items_ordered'])
        )
    conn.commit()
    cur.close()
    conn.close()

def load_store_performance(**kwargs):
    data = kwargs['ti'].xcom_pull(key='transformed_store_performance_data', task_ids='transform_store_performance')
    df = pd.DataFrame(data)

    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )

    cur = conn.cursor()
    for index, row in df.iterrows():
        cur.execute(
            """
            INSERT INTO fact_store_performance (date, store_name, total_sales, total_customers)
            VALUES (%s, %s, %s, %s)
            """,
            (row['date'], row['store_name'], row['total_sales'], row['total_customers'])
        )
    conn.commit()
    cur.close()
    conn.close()

# Define the tasks
extract_sales_task = PythonOperator(
    task_id='extract_sales',
    python_callable=extract_sales,
    provide_context=True,
    dag=dag,
)

extract_inventory_task = PythonOperator(
    task_id='extract_inventory',
    python_callable=extract_inventory,
    provide_context=True,
    dag=dag,
)

extract_customer_orders_task = PythonOperator(
    task_id='extract_customer_orders',
    python_callable=extract_customer_orders,
    provide_context=True,
    dag=dag,
)

extract_store_performance_task = PythonOperator(
    task_id='extract_store_performance',
    python_callable=extract_store_performance,
    provide_context=True,
    dag=dag,
)

transform_sales_task = PythonOperator(
    task_id='transform_sales',
    python_callable=transform_sales,
    provide_context=True,
    dag=dag,
)

transform_inventory_task = PythonOperator(
    task_id='transform_inventory',
    python_callable=transform_inventory,
    provide_context=True,
    dag=dag,
)

transform_customer_orders_task = PythonOperator(
    task_id='transform_customer_orders',
    python_callable=transform_customer_orders,
    provide_context=True,
    dag=dag,
)

transform_store_performance_task = PythonOperator(
    task_id='transform_store_performance',
    python_callable=transform_store_performance,
    provide_context=True,
    dag=dag,
)

load_sales_task = PythonOperator(
    task_id='load_sales',
    python_callable=load_sales,
    provide_context=True,
    dag=dag,
)

load_inventory_task = PythonOperator(
    task_id='load_inventory',
    python_callable=load_inventory,
    provide_context=True,
    dag=dag,
)

load_customer_orders_task = PythonOperator(
    task_id='load_customer_orders',
    python_callable=load_customer_orders,
    provide_context=True,
    dag=dag,
)

load_store_performance_task = PythonOperator(
    task_id='load_store_performance',
    python_callable=load_store_performance,
    provide_context=True,
    dag=dag,
)

# Define the task dependencies
extract_sales_task >> transform_sales_task >> load_sales_task
extract_inventory_task >> transform_inventory_task >> load_inventory_task
extract_customer_orders_task >> transform_customer_orders_task >> load_customer_orders_task
extract_store_performance_task >> transform_store_performance_task >> load_store_performance_task
