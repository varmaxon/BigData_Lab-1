-- stg_customers: чистим и типизируем сырые данные клиентов

SELECT
    customer_id,
    name                            AS customer_name,
    city,
    segment,
    created_at::date                AS signup_date
FROM read_parquet('{{ env_var("LAB_DIR", "..") }}/data/raw_customers.parquet')
