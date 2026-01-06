SET search_path TO warehouse;

CREATE TABLE IF NOT EXISTS dim_date (
    date_id DATE PRIMARY KEY,
    year INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL,
    day_of_week INT NOT NULL,
    day_name VARCHAR NOT NULL,
    month_name VARCHAR NOT NULL,
    quarter INT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_staff (
    staff_id INT PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    department_name VARCHAR NOT NULL,
    location VARCHAR NOT NULL,
    email_address VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_location (
    location_id INT PRIMARY KEY,
    address_line_1 VARCHAR NOT NULL,
    address_line_2 VARCHAR,
    district VARCHAR,
    city VARCHAR NOT NULL,
    postal_code VARCHAR NOT NULL,
    country VARCHAR NOT NULL,
    phone VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_currency (
    currency_id INT PRIMARY KEY,
    currency_code VARCHAR(3) NOT NULL,
    currency_name VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_design (
    design_id INT PRIMARY KEY,
    design_name VARCHAR NOT NULL,
    file_location VARCHAR NOT NULL,
    file_name VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_counterparty (
    counterparty_id INT PRIMARY KEY,
    counterparty_legal_name VARCHAR NOT NULL,
    counterparty_legal_address_line_1 VARCHAR NOT NULL,
    counterparty_legal_address_line_2 VARCHAR,
    counterparty_legal_district VARCHAR,
    counterparty_legal_city VARCHAR NOT NULL,
    counterparty_legal_postal_code VARCHAR NOT NULL,
    counterparty_legal_country VARCHAR NOT NULL,
    counterparty_legal_phone_number VARCHAR NOT NULL
);
