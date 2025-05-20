-- Create the inventory database
CREATE DATABASE IF NOT EXISTS inventory;

-- Switch to the inventory database
USE inventory;

-- Drop tables if they already exist (for fresh setup)
DROP TABLE IF EXISTS Inventory;

-- Create Inventory table
CREATE TABLE Inventory (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(100),
    quantity INT NOT NULL CHECK (quantity >= 0)
);

-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS UpdateInventory;

DELIMITER //
CREATE PROCEDURE UpdateInventory(
    IN product_ids JSON,
    IN quantities JSON
)
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE total INT;
    DECLARE prod_id VARCHAR(50);
    DECLARE qty INT;
    DECLARE current_qty INT;

    -- Start a transaction
    START TRANSACTION;

    -- Get the number of items in the JSON arrays
    SET total = JSON_LENGTH(product_ids);

    -- Loop through the JSON arrays of product IDs and quantities
    WHILE i < total DO
        -- Extract product_id and quantity
        SET prod_id = JSON_UNQUOTE(JSON_EXTRACT(product_ids, CONCAT('$[', i, ']')));
        SET qty = JSON_EXTRACT(quantities, CONCAT('$[', i, ']'));

        -- Check current stock with row-level locking
        SELECT quantity INTO current_qty
        FROM Inventory
        WHERE product_id = prod_id
        FOR UPDATE;

        -- If insufficient stock, rollback and exit
        IF current_qty < qty THEN
            ROLLBACK;
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient stock for product';
        END IF;

        -- Deduct the quantity from the inventory
        UPDATE Inventory
        SET quantity = quantity - qty
        WHERE product_id = prod_id;

        -- Move to the next item
        SET i = i + 1;
    END WHILE;

    -- Commit transaction if all updates succeed
    COMMIT;
END //
DELIMITER ;