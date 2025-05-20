from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('MY_SQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE'),
            port=int(os.getenv('MYSQL_PORT', 3306)),
            autocommit=False,
        )
        print("Database connection successful")
        return conn
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

# Product model
class Product(BaseModel):
    product_id: str
    product_name: str
    quantity: int

# Update inventory model
class UpdateInventoryRequest(BaseModel):
    product_ids: list[str]
    quantities: list[int]

# Add a new product to the inventory
@app.post("/add-product")
async def add_product(product: Product):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO Inventory (product_id, product_name, quantity) VALUES (%s, %s, %s)"
        cursor.execute(sql, (product.product_id, product.product_name, product.quantity))
        conn.commit()
        cursor.close()
        print(f"Product {product.product_id} added to inventory.")
        return {"message": "Product added successfully"}
    except mysql.connector.Error as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conn:
            conn.close()

# Get all products from the inventory
@app.get("/products")
async def get_products():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Get results as dictionaries
        cursor.execute("SELECT * FROM Inventory")
        products = cursor.fetchall()
        cursor.close()
        return {"products": products}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

# Update inventory using stored procedure
@app.put("/update-inventory")
async def update_inventory(request: UpdateInventoryRequest):
    conn = None
    try:
        # Validate that product_ids and quantities lists are of the same length
        if len(request.product_ids) != len(request.quantities):
            raise HTTPException(
                status_code=400,
                detail="Product IDs and quantities lists must be of the same length"
            )

        conn = get_db_connection()
        cursor = conn.cursor()
        product_ids_json = json.dumps(request.product_ids)
        quantities_json = json.dumps(request.quantities)

        # Call the stored procedure
        print("Calling stored procedure...")
        cursor.callproc('UpdateInventory', (product_ids_json, quantities_json))
        conn.commit()
        cursor.close()
        print(f"Inventory updated for products: {request.product_ids}")
        return {"message": "Inventory updated successfully", "status": True}
    except mysql.connector.Error as e:
        if conn:
            conn.rollback()
        if "Insufficient stock" in str(e):
            return {"error": str(e), "status": False}
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

# Basic health check endpoint
@app.get("/")
async def health_check():
    return {"status": "ok"}

@app.get("/get")
async def getFunc():
    return {"status": "everything fine"}
