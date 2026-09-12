-- MySQL schema for the Purchase Order app.
-- Replaces the original Oracle CUSTOMER / PRODUCTORDER / PAYMENT tables.
-- Run with:  mysql -u root -p < db/schema.sql

CREATE DATABASE IF NOT EXISTS purchase_order
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE purchase_order;

CREATE TABLE IF NOT EXISTS CUSTOMER (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name  VARCHAR(50)  NOT NULL,
    last_name   VARCHAR(50)  NOT NULL,
    email       VARCHAR(100) NOT NULL,
    street1     VARCHAR(100) NOT NULL,
    street2     VARCHAR(100),
    city        VARCHAR(50)  NOT NULL,
    state       VARCHAR(50)  NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS PRODUCT (
    pid         VARCHAR(10) PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    price       DECIMAL(10, 2) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS PRODUCTORDER (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id      VARCHAR(30) NOT NULL,
    pid           VARCHAR(10) NOT NULL,
    FOREIGN KEY (pid) REFERENCES PRODUCT(pid)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS PAYMENT (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id   VARCHAR(30) NOT NULL UNIQUE,
    amount     DECIMAL(10, 2) NOT NULL,
    pay_mode   VARCHAR(30) NOT NULL,
    paid_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Seed the product catalog used by the Purchase Order screen
-- (kept in sync with app/products.py).
INSERT INTO PRODUCT (pid, name, description, price) VALUES
    ('P-01', 'Cap',        'This product is made from at least 50% recycled polyester fiber', 100.00),
    ('P-02', 'Linen Shoe', 'You will wear it again and again, this shoe is remarkable and loyal just like you', 1200.00),
    ('P-03', 'Hoodie',     'Durably stitched surfaces, clean finishes and the perfect amount of shine to make you dazzle', 800.00)
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    description = VALUES(description),
    price = VALUES(price);
