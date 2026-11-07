-- fct_revenue: витрина выручки по месяцам и сегментам
--
-- TODO: Напишите запрос, который:
--   1. Соединяет "warehouse"."main"."stg_orders" с "warehouse"."main"."stg_customers"
--   2. Группирует по: месяцу заказа (date_trunc('month', order_date))
--      и сегменту клиента (segment)
--   3. Считает:
--      - total_orders    — количество заказов
--      - total_revenue   — сумма amount
--      - avg_order_value — средняя сумма заказа
--      - cancelled_pct   — доля cancelled (0.0 – 1.0)
--   4. Учитывает только заказы со статусом 'shipped' для total_revenue
--      (используйте FILTER или CASE WHEN)

SELECT
    date_trunc('month', o.order_date)::date          AS month,
    c.segment,
    count(*)                                         AS total_orders,
    round(sum(
        CASE WHEN o.status = 'shipped' THEN o.amount ELSE 0 END
    ), 2)                                            AS total_revenue,
    round(avg(o.amount), 2)                          AS avg_order_value,
    round(
        count(*) FILTER (WHERE o.status = 'cancelled')::float / count(*),
        3
    )                                                AS cancelled_pct
FROM "warehouse"."main"."stg_orders"    AS o
JOIN "warehouse"."main"."stg_customers" AS c USING (customer_id)
GROUP BY 1, 2
ORDER BY 1, 2