from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import mysql.connector
import os

app = FastAPI()

class CartItem(BaseModel):
    product_id: int
    quantity: int
    price: int

class OrderRequest(BaseModel):
    username: str
    cart: List[CartItem]

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=os.getenv("MYSQL_PORT"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB")
    )

@app.post("/make_order")
def create_order(order: OrderRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Insert into user_orders and get the generated order_id
        cursor.execute("INSERT INTO user_orders (username) VALUES (%s)", (order.username,))
        order_id = cursor.lastrowid

        # Insert each item into order_details
        for item in order.cart:
            cursor.execute("""
                INSERT INTO order_details (order_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """, (order_id, item.product_id, item.quantity, item.price))

        conn.commit()
        return {"message": "Order placed successfully", "order_id": order_id}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
