-- Топ-5 товаров по выручке за последние 3 календарных месяца.
-- За последнюю дату берём максимальную дату заказа в наборе данных.

WITH last_month AS (
    SELECT date_trunc('month', max(order_date)) AS month
    FROM {{ ref('stg_orders') }}
)
SELECT
    o.product,
    o.category,
    round(sum(o.amount), 2) AS total_revenue,
    count(*) AS order_count,
    round(avg(o.discount), 3) AS avg_discount
FROM {{ ref('stg_orders') }} AS o
CROSS JOIN last_month AS m
WHERE o.status = 'shipped'
  AND o.order_date >= m.month - INTERVAL '2 months'
  AND o.order_date < m.month + INTERVAL '1 month'
GROUP BY o.product, o.category
ORDER BY total_revenue DESC, o.product
LIMIT 5
