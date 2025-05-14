CREATE DATABASE IF NOT EXISTS orders;

USE orders;

CREATE TABLE
    IF NOT EXISTS user_orders (
        username VARCHAR(255) NOT NULL,
        order_id INT AUTO_INCREMENT PRIMARY KEY
    );

CREATE TABLE
    IF NOT EXISTS order_details (
        order_id INT NOT NULL,
        product_id INT NOT NULL,
        quantity INT NOT NULL,
        price INT NOT NULL,
        FOREIGN KEY (order_id) REFERENCES user_orders (order_id)
    );