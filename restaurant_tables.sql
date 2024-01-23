DROP DATABASE IF EXISTS restaurant;
CREATE DATABASE restaurant;
use restaurant;

CREATE TABLE customer_statistics (
    customer_id INT PRIMARY KEY,
    total_orders INT,
    total_items INT,
    total_spent FLOAT(2)
);

CREATE TABLE orders (
    order_id VARCHAR(40) PRIMARY KEY,
    customer_id INT,
    items INT,
    aperitifs VARCHAR(30),
    appetizers VARCHAR(30),
    entrees VARCHAR(30),
    desserts VARCHAR(30),
    total VARCHAR(30),
    FOREIGN KEY (customer_id) REFERENCES customer_statistics(customer_id)
);

CREATE TABLE customer_demographics (
    customer_demographic_id VARCHAR(40) PRIMARY KEY,
    address VARCHAR(95),
    city VARCHAR(35),
    credit_card_expires CHAR(5),
    credit_card_number VARCHAR(19),
    credit_card_provider VARCHAR(50),
    credit_card_security_code INT,
    email VARCHAR(62),
    name VARCHAR(50),
    phone_number VARCHAR(30),
    state VARCHAR(50),
    zip_code INT,
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES customer_statistics(customer_id)
);
