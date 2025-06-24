-- TODO: This query will return a table with the top 10 revenue categories in 
-- English, the number of orders and their total revenue. The first column will 
-- be Category, that will contain the top 10 revenue categories; the second one 
-- will be Num_order, with the total amount of orders of each category; and the 
-- last one will be Revenue, with the total revenue of each catgory.
-- HINT: All orders should have a delivered status and the Category and actual 
-- delivery date should be not null.
SELECT
    pct.product_category_name_english AS Category,
    COUNT(DISTINCT lo.order_id) AS Num_order,
    SUM(op.payment_value) AS Revenue
FROM
    olist_orders lo
    JOIN olist_order_items oi ON lo.order_id = oi.order_id
    JOIN olist_products pdt ON oi.product_id = pdt.product_id
    JOIN product_category_name_translation pct ON pdt.product_category_name = pct.product_category_name
    JOIN olist_order_payments op ON lo.order_id = op.order_id
WHERE
    lo.order_status = 'delivered'
    AND lo.order_delivered_customer_date IS NOT NULL
    AND pdt.product_category_name IS NOT NULL
GROUP BY
    pct.product_category_name_english
ORDER BY
    Revenue DESC
LIMIT 10;
