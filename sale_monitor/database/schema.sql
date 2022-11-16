DROP TABLE IF EXISTS watched_products;
DROP TABLE IF EXISTS contact_details;


CREATE TABLE contact_details (
    email TEXT PRIMARY KEY,
    location_id TEXT NOT NULL DEFAULT '',   -- empty string indicates not store chosen.
    chain TEXT NOT NULL DEFAULT '',         -- e.g. Kroger
    address1 TEXT NOT NULL DEFAULT '',
    city TEXT NOT NULL DEFAULT '',
    state TEXT NOT NULL DEFAULT '',
    zipcode TEXT NOT NULL DEFAULT ''
);

CREATE TABLE watched_products (

    watched_product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_email TEXT NOT NULL,
    product_upc TEXT NOT NULL,
    product_description TEXT NOT NULL,
    normal_price TEXT NOT NULL,
    promo_price TEXT NOT NULL,
    target_price TEXT NOT NULL,
    last_discount_rate FLOAT DEFAULT 0,       --  Percentage off from full price
    timestamp_last_checked INTEGER,
    image_url TEXT NOT NULL,

    FOREIGN KEY (contact_email) REFERENCES contact_details(email)
);