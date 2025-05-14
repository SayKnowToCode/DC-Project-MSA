from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="ecommerce_db"
)

# Product model
class Product(BaseModel):
    product_id: int
    product_name: str
    description: str
    price: float
    quantity: int

@app.get("/validate/{product_id}/{quantity}")
async def validate_product(product_id: int, quantity: int):
    cursor = db.cursor()

    try:
        # Call stored procedure to check product availability
        result = cursor.callproc("check_and_update_stock", (product_id, quantity, 0))
        available = list(cursor.stored_results())[0].fetchone()[0]
        print(result)
        print(f"Product {product_id} availability: {available}")
        if not available:
            raise HTTPException(status_code=400, detail=f"Product {product_id} is out of stock.")

        cursor.execute("SELECT price FROM products WHERE product_id = %s", (product_id,))
        print(f"Product {product_id} price: {cursor.fetchone()[0]}")
        return {"status": "success", "message": "Product available", "price": cursor.fetchone()[0]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inventory check failed: {str(e)}")

    finally:
        cursor.close()

@app.post("/add_product/")
async def add_product(product: Product):
    cursor = db.cursor()

    try:
        # Insert the new product into the inventory
        cursor.execute("INSERT INTO products (product_id, product_name, quantity) VALUES (%s, %s, %s)",
                       (product.product_id, product.product_name, product.quantity))
        db.commit()
        return {"message": "Product added successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add product: {str(e)}")

    finally:
        cursor.close()

@app.get("/")
def health_check():
    return {"status": "Inventory Service is running"}
