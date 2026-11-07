
  
  create view "warehouse"."main"."stg_customers__dbt_tmp" as (
    -- stg_customers: чистим и типизируем сырые данные клиентов

SELECT
    customer_id,
    name                            AS customer_name,
    city,
    segment,
    created_at::date                AS signup_date
FROM read_parquet('F:\BMSTU\!МАГИСТРАТУРА\3_semester\Сбер\ЛР1\lab/data/raw_customers.parquet')
  );
