-- Create database if not exists
CREATE DATABASE IF NOT EXISTS ecommerce_db;
USE ecommerce_db;

-- Products table (Inventory)
CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    product_description TEXT,
    price DECIMAL(10, 2),
    quantity INT
);

-- Stored Procedure to check product availability and update
DELIMITER //
CREATE PROCEDURE check_and_update_stock(IN p_id INT, IN p_qty INT, OUT is_available BOOLEAN)
BEGIN
    DECLARE available_qty INT;
    
    -- Check availability
    SELECT quantity INTO available_qty FROM products WHERE product_id = p_id;

    IF available_qty IS NULL OR available_qty < p_qty THEN
        SET is_available = FALSE;
    ELSE
        -- Update the stock
        UPDATE products SET quantity = quantity - p_qty WHERE product_id = p_id;
        SET is_available = TRUE;
    END IF;
END //
DELIMITER ;
