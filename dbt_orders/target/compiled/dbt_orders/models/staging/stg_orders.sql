-- stg_orders: стейджинг-модель заказов
--
-- TODO: Заполните SELECT-список, используя колонки из raw_orders:
--   order_id, customer_id, product, category, quantity,
--   unit_price, discount, amount, status, order_date, created_at
--
-- Требования:
--   1. Переименуйте created_at → loaded_at
--   2. Добавьте вычисляемое поле: is_completed = (status = 'shipped')
--   3. Отфильтруйте строки, где amount <= 0

SELECT
    order_id,
    customer_id,
    product,
    category,
    quantity,
    unit_price,
    discount,
    amount,
    status,
    (status = 'shipped')            AS is_completed,
    order_date,
    created_at                      AS loaded_at
FROM read_parquet('F:\BMSTU\!МАГИСТРАТУРА\3_semester\Сбер\ЛР1\lab/data/raw_orders.parquet')
WHERE amount > 0