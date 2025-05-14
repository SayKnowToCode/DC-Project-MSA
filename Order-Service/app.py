from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import mysql.connector
import requests
import os

app = FastAPI()

db = mysql.connector.connect(
    host=os.environ["MYSQL_HOST"],
    user=os.environ["MYSQL_USER"],
    password=os.environ["MYSQL_PASSWORD"],
    database=os.environ["MYSQL_DB"],
    port=int(os.environ["MYSQL_PORT"]),
)


# Request models
class ProductItem(BaseModel):
    product_id: int
    quantity: int

class OrderRequest(BaseModel):
    username: str
    cart: List[ProductItem]

def next_order_id(cursor):
    cursor.execute("SELECT COALESCE(MAX(order_id), 0) + 1 FROM orders")
    return cursor.fetchone()[0]

@app.post("/place_order/")
async def place_order(order_request: OrderRequest):
    cursor = db.cursor()
    print("Received order request:", order_request)

    try:
        total_amount = 0
        validated_items = []

        for item in order_request.cart:
            response = requests.get(f"http://dc-project.com/inventory/validate/{item.product_id}/{item.quantity}")
            print("Inventory service response:", response.json())

            if response.status_code != 200:
                print(f"Product {item.product_id} is out of stock.")
                return {"message": f"Product {item.product_id} out of stock."}

            response_data = response.json()
            validated_items.append((item.product_id, item.quantity, response_data['price']))
            total_amount += response_data['price'] * item.quantity
            print(f"Product {item.product_id} validated successfully. Total amount so far: {total_amount}")

        order_id = next_order_id(cursor)

        cursor.execute("START TRANSACTION")
        cursor.execute("INSERT INTO orders (username, total_amount) VALUES (%s, %s)", (order_request.username, total_amount))

        for product_id, quantity, price in validated_items:
            cursor.execute("INSERT INTO ordered_products (order_id, product_id, quantity) VALUES (%s, %s, %s)", 
                           (order_id, product_id, quantity))

        db.commit()
        print("Order placed successfully")
        return {"message": "Order placed successfully", "order_id": order_id}

    except Exception as e:
        db.rollback()
        print("Error during order placement:", str(e))
        raise HTTPException(status_code=500, detail=f"Order placement failed: {str(e)}")

    finally:
        cursor.close()

@app.get("/orders/{username}")
async def get_orders(username: str):
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM ordered_product WHERE order_id IN (SELECT order_id FROM orders WHERE username = %s)", (username,))
        orders = cursor.fetchall()
        print("Fetched orders:", orders)
        
        if not orders:
            raise HTTPException(status_code=404, detail="No orders found for this user")
        return {"orders": orders}
    except Exception as e:
        print("Error fetching orders:", str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch orders")
    finally:
        cursor.close()


@app.get("/")
def health_check():
    return {"status": "Order Service is running"}
