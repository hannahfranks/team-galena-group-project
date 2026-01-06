SET search_path TO warehouse;

CREATE TABLE IF NOT EXISTS fact_sales_order (
    sales_record_id SERIAL PRIMARY KEY,
    sales_order_id INT NOT NULL,

    created_date DATE NOT NULL,
    created_time TIME NOT NULL,
    last_updated_date DATE NOT NULL,
    last_updated_time TIME NOT NULL,

    sales_staff_id INT NOT NULL,
    counterparty_id INT NOT NULL,
    units_sold INT NOT NULL,
    unit_price NUMERIC(10,2) NOT NULL,
    currency_id INT NOT NULL,
    design_id INT NOT NULL,

    agreed_payment_date DATE NOT NULL,
    agreed_delivery_date DATE NOT NULL,
    agreed_delivery_location_id INT NOT NULL,

    CONSTRAINT fk_created_date
        FOREIGN KEY (created_date) REFERENCES dim_date(date_id),

    CONSTRAINT fk_last_updated_date
        FOREIGN KEY (last_updated_date) REFERENCES dim_date(date_id),

    CONSTRAINT fk_sales_staff
        FOREIGN KEY (sales_staff_id) REFERENCES dim_staff(staff_id),

    CONSTRAINT fk_counterparty
        FOREIGN KEY (counterparty_id) REFERENCES dim_counterparty(counterparty_id),

    CONSTRAINT fk_currency
        FOREIGN KEY (currency_id) REFERENCES dim_currency(currency_id),

    CONSTRAINT fk_design
        FOREIGN KEY (design_id) REFERENCES dim_design(design_id),

    CONSTRAINT fk_payment_date
        FOREIGN KEY (agreed_payment_date) REFERENCES dim_date(date_id),

    CONSTRAINT fk_delivery_date
        FOREIGN KEY (agreed_delivery_date) REFERENCES dim_date(date_id),

    CONSTRAINT fk_delivery_location
        FOREIGN KEY (agreed_delivery_location_id)
        REFERENCES dim_location(location_id)
);
