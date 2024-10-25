CREATE TABLE clothing (
    id SERIAL PRIMARY KEY,
    brand VARCHAR(100),
    fabric VARCHAR(100),
    age INT,
    original_price DECIMAL,
    current_price DECIMAL
                      );