CREATE TABLE IF NOT EXISTS product (
    product_id SERIAL NOT NULL,
    name varchar(250) NOT NULL,
    price numeric NOT NULL,
    create_at timestamp default current_timestamp,
    PRIMARY KEY (product_id)
);