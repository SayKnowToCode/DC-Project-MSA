-- Create database if not exists
CREATE DATABASE IF NOT EXISTS ecommerce_db;

-- Use the database
USE ecommerce_db;

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
);

-- Ordered products table
CREATE TABLE IF NOT EXISTS ordered_products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);