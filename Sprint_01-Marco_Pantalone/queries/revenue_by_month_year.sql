-- TODO: This query will return a table with the revenue by month and year. It
-- will have different columns: month_no, with the month numbers going from 01
-- to 12; month, with the 3 first letters of each month (e.g. Jan, Feb);
-- Year2016, with the revenue per month of 2016 (0.00 if it doesn't exist);
-- Year2017, with the revenue per month of 2017 (0.00 if it doesn't exist) and
-- Year2018, with the revenue per month of 2018 (0.00 if it doesn't exist).
WITH months AS (
  SELECT '01' AS month_no UNION ALL SELECT '02' UNION ALL SELECT '03' UNION ALL
  SELECT '04' UNION ALL SELECT '05' UNION ALL SELECT '06' UNION ALL
  SELECT '07' UNION ALL SELECT '08' UNION ALL SELECT '09' UNION ALL
  SELECT '10' UNION ALL SELECT '11' UNION ALL SELECT '12'
),
month_names AS (
  SELECT '01' AS month_no, 'Jan' AS month UNION ALL
  SELECT '02', 'Feb' UNION ALL SELECT '03', 'Mar' UNION ALL
  SELECT '04', 'Apr' UNION ALL SELECT '05', 'May' UNION ALL SELECT '06', 'Jun' UNION ALL
  SELECT '07', 'Jul' UNION ALL SELECT '08', 'Aug' UNION ALL SELECT '09', 'Sep' UNION ALL
  SELECT '10', 'Oct' UNION ALL SELECT '11', 'Nov' UNION ALL SELECT '12', 'Dec'
),
min_payments AS (
  SELECT 
    order_id,
    MIN(payment_value) AS min_payment
  FROM olist_order_payments
  GROUP BY order_id
),
revenue AS (
  SELECT
    STRFTIME('%m', o.order_delivered_customer_date) AS month_no,
    STRFTIME('%Y', o.order_delivered_customer_date) AS year,
    SUM(mp.min_payment) AS total_revenue
  FROM olist_orders o
  JOIN min_payments mp ON o.order_id = mp.order_id
  WHERE o.order_status = 'delivered'
    AND o.order_delivered_customer_date IS NOT NULL
    AND STRFTIME('%Y', o.order_delivered_customer_date) IN ('2016', '2017', '2018')
  GROUP BY month_no, year
)
SELECT
  m.month_no,
  mn.month,
  COALESCE(MAX(CASE WHEN r.year = '2016' THEN r.total_revenue END), 0.0) AS Year2016,
  COALESCE(MAX(CASE WHEN r.year = '2017' THEN r.total_revenue END), 0.0) AS Year2017,
  COALESCE(MAX(CASE WHEN r.year = '2018' THEN r.total_revenue END), 0.0) AS Year2018
FROM months m
JOIN month_names mn ON m.month_no = mn.month_no
LEFT JOIN revenue r ON m.month_no = r.month_no
GROUP BY m.month_no, mn.month
ORDER BY m.month_no;