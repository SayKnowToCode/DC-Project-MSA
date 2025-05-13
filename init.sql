-- Create auth DB and users table
CREATE DATABASE IF NOT EXISTS auth;

USE auth;

CREATE TABLE
    IF NOT EXISTS users (
        username VARCHAR(255) PRIMARY KEY,
        password VARCHAR(255) NOT NULL
    );

-- Create products DB and products table
CREATE DATABASE IF NOT EXISTS products;

USE products;

CREATE TABLE
    IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        price DECIMAL(10, 2)
    );

-- Insert sample products
INSERT INTO
    products (name, description, price)
VALUES
    ('Product 1', 'A demo product 1', 10.00),
    ('Product 2', 'A demo product 2', 20.50),
    ('Product 3', 'A demo product 3', 15.75),
    ('Product 4', 'A demo product 4', 99.99),
    ('Product 5', 'A demo product 5', 5.25);