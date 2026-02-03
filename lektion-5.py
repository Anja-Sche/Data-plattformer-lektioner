from fastapi import FastAPI, status
from psycopg_pool import ConnectionPool
from psycopg.types.json import Json # Convert Pydantic -> JSON
from psycopg import Connection      # Open Temporary Connection

from schema.product import ProductSchema

DATABASE_URL = "postgresql://postgres:roligt@localhost:5433/lektion_5"
pool = ConnectionPool(DATABASE_URL)

app = FastAPI(title="lektion_5_postgresql_fastapi")

@app.get("/")
def root() -> dict:
    return {"Hello": "World"}

@app.post("/products",
          status_code=status.HTTP_201_CREATED,
          response_model=ProductSchema,
          )
def post_product(product: ProductSchema) -> ProductSchema:

    # Query-Insert
    with pool.connection() as conn:
        insert_product(conn, product.model_dump())
        conn.commit()  # Execute Logic (close connection when done)

    return product



# Helper Mehtod for DB-Querys
def insert_product(conn: Connection, product:ProductSchema):
    conn.execute(
        "INSERT INTO products_raw(product) VALUES (%s)",
        (Json(product),)  # TODO : Explore the syntax
    )

@app.get("/products" )
def get_products ():
    with pool.connection () as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT product FROM products_raw" )
            rows = cur.fetchall()

    # rows = [(product_dict,), (product_dict,), ...]
    return [row[0] for row in rows]
