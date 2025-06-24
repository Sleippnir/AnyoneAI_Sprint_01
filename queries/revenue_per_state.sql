-- TODO: This query will return a table with two columns; customer_state, and 
-- Revenue. The first one will have the letters that identify the top 10 states 
-- with most revenue and the second one the total revenue of each.
-- HINT: All orders should have a delivered status and the actual delivery date 
-- should be not null. 
SELECT
    c.customer_state,
    SUM(op.payment_value) AS Revenue
FROM
    olist_orders lo
    JOIN olist_customers c ON lo.customer_id = c.customer_id
    JOIN olist_order_payments op ON lo.order_id = op.order_id
WHERE
    lo.order_status = 'delivered'
    AND lo.order_delivered_customer_date IS NOT NULL
GROUP BY
    c.customer_state
ORDER BY
    Revenue DESC
LIMIT 10;
