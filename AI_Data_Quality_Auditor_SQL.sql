CREATE DATABASE ai_data_auditor;
USE ai_data_auditor;

CREATE TABLE dirty_orders (
    order_id VARCHAR(20),
    customer_id VARCHAR(20),
    customer_name VARCHAR(100),
    email VARCHAR(150),
    phone VARCHAR(20),
    city VARCHAR(50),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    product_name VARCHAR(100),
    category VARCHAR(50),
    quantity VARCHAR(20),
    unit_price_inr VARCHAR(30),
    order_date VARCHAR(30),
    payment_method VARCHAR(50),
    order_status VARCHAR(50)
);

DESCRIBE dirty_orders;

USE ai_data_auditor;

SELECT COUNT(*) AS total_records
FROM dirty_orders;

SELECT *
FROM dirty_orders
LIMIT 20;

SELECT *
FROM dirty_orders
WHERE email IS NULL OR TRIM(email) = ''
   OR state IS NULL OR TRIM(state) = ''
   OR product_name IS NULL OR TRIM(product_name) = '';
   
SELECT order_id, COUNT(*) AS duplicate_count
FROM dirty_orders
GROUP BY order_id
HAVING COUNT(*) > 1;

SELECT order_id, email
FROM dirty_orders
WHERE email IS NOT NULL
AND TRIM(email) != ''
AND email NOT REGEXP
'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$';

SELECT order_id, phone
FROM dirty_orders
WHERE phone NOT REGEXP '^[6-9][0-9]{9}$';

SELECT order_id, quantity
FROM dirty_orders
WHERE CAST(quantity AS SIGNED) <= 0
   OR CAST(quantity AS SIGNED) > 10;
   
SELECT order_id, unit_price_inr
FROM dirty_orders
WHERE CAST(unit_price_inr AS DECIMAL(10,2)) <= 0
   OR CAST(unit_price_inr AS DECIMAL(10,2)) > 100000;
   
SELECT DISTINCT order_status
FROM dirty_orders;

SELECT DISTINCT payment_method
FROM dirty_orders;

SELECT DISTINCT order_status
FROM dirty_orders;

SELECT order_id, order_date
FROM dirty_orders
WHERE STR_TO_DATE(order_date, '%d-%m-%Y') IS NULL;

SELECT order_id, order_date
FROM dirty_orders
WHERE STR_TO_DATE(order_date, '%d-%m-%Y') > CURDATE();

SELECT order_id, postal_code
FROM dirty_orders
WHERE postal_code NOT REGEXP '^[0-9]{6}$';

SELECT order_id, city, state
FROM dirty_orders
WHERE (city = 'Nagpur' AND state != 'Maharashtra')
   OR (city = 'Mumbai' AND state != 'Maharashtra')
   OR (city = 'Pune' AND state != 'Maharashtra')
   OR (city = 'Delhi' AND state != 'Delhi')
   OR (city = 'Bengaluru' AND state != 'Karnataka')
   OR (city = 'Hyderabad' AND state != 'Telangana')
   OR (city = 'Ahmedabad' AND state != 'Gujarat')
   OR (city = 'Jaipur' AND state != 'Rajasthan')
   OR (city = 'Kolkata' AND state != 'West Bengal')
   OR (city = 'Chennai' AND state != 'Tamil Nadu');
   
SELECT order_id, product_name, category
FROM dirty_orders
WHERE (product_name IN ('Wireless Mouse','Bluetooth Speaker')
       AND category != 'Electronics')
   OR (product_name IN ('Cotton Kurta','Running Shoes')
       AND category != 'Fashion')
   OR (product_name IN ('Water Bottle','Bedsheet Set')
       AND category != 'Home')
   OR (product_name IN ('Face Serum','Shampoo')
       AND category != 'Beauty')
   OR (product_name IN ('Notebook Pack','Desk Organizer')
       AND category != 'Stationery');
       
SELECT customer_id,
       COUNT(DISTINCT customer_name) AS names,
       COUNT(DISTINCT email) AS emails,
       COUNT(DISTINCT phone) AS phones
FROM dirty_orders
GROUP BY customer_id
HAVING names > 1 OR emails > 1 OR phones > 1;

SELECT
    COUNT(*) AS total_rows,

    SUM(email IS NULL OR TRIM(email) = '') AS missing_emails,

    SUM(state IS NULL OR TRIM(state) = '') AS missing_states,

    SUM(product_name IS NULL OR TRIM(product_name) = '')
        AS missing_products,

    SUM(phone NOT REGEXP '^[6-9][0-9]{9}$')
        AS invalid_phones,

    SUM(postal_code NOT REGEXP '^[0-9]{6}$')
        AS invalid_postal_codes,

    SUM(CAST(quantity AS SIGNED) <= 0)
        AS invalid_quantities,

    SUM(CAST(quantity AS SIGNED) > 10)
        AS quantity_outliers,

    SUM(CAST(unit_price_inr AS DECIMAL(10,2)) <= 0)
        AS invalid_prices,

    SUM(CAST(unit_price_inr AS DECIMAL(10,2)) > 100000)
        AS price_outliers

FROM dirty_orders;

