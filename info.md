# postgres and fastapi

## installation
* pip install "fastapi[standard]"
* pip install "psycopg[binary]"
* pip install "psycopg[pool]"

## Run app
* `$ fastapi dev filnamn.py`

## sorting data -philosophy

* What's the purpose of our data?
    * bulk uploading
    * JSON data storage
    * unorganized data
    * PostgreSQL database
* what's the datatype of said data?
    * Unorganized
    * Unstructiúred
    * Json

## Database - PostgreSQL
A newly created database does not contain any tables by default

Step #1 - Create new Table (products)
```postgresql
CREATE TABLE IF NOT EXISTS  products_raw (
id BIGSERIAL PRIMARY KEY,
created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
product JSONB NOT NULL
);
```

Step #2 - Create a connection with the database using URL
Assuming you're using PGadmin4 you can find the required data like so:
* Right-click your own database -> properties -> username
* Password: You should know this one
* Port: Right-klick PostgreSQL 17 -> properties -> connection -> port
* Address: Same steps as port

```python
DATABASE_URL = "postgresql://USERNAME:PASSWORD@ADDRESS:PORT/DB_NAME"
```

Step #3 - Implement function for Insert (fastAPI)

```python
def insert_product(conn: Connection, product:ProductSchema):
    conn.execute(
        "INSERT INTO products_raw(product) VALUES (%s)",
        (Json(product),)  # TODO : Explore the syntax
    )
```

```python
@app.post("/products",
          status_code=status.HTTP_201_CREATED,
          response_model=ProductSchema,
          )
def post_product(product: ProductSchema) -> ProductSchema:

    # Query-Insert
    with pool.connection() as conn:
        insert_product(conn, product)
        conn.commit()  # Execute Logic (close connection when done)


    return product
```

Postman Test against 'localhost:8000/products'
```json
{
    "product_id": "USP239",
    "name": "Wireless Mouse",
    "price": 249.0,
    "currency": "SEK",
    "category": "Electronics",
    "brand": null
}
```