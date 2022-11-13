DROP TABLE IF EXISTS watched_products;
DROP TABLE IF EXISTS contact_details;


CREATE TABLE contact_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    location_id TEXT NOT NULL,
    chain TEXT NOT NULL,  -- e.g. Kroger
    address1 TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zipcode TEXT NOT NULL
);

CREATE TABLE watched_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_id INTEGER NOT NULL,
    product_upc TEXT NOT NULL,
    target_price FLOAT NOT NULL,
    last_discount_rate FLOAT DEFAULT 0,       --  Percentage off from full price

    FOREIGN KEY (contact_id) REFERENCES contact_details(id)
);


--- Simplify error handling and whatever. Just assume there is always 1 entry in the contact_details table.
INSERT INTO contact_details
VALUES (1, 'email', '', 'chain', 'address1', 'city', 'state', 'zipcode')