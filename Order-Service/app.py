from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import mysql.connector
import requests

app = FastAPI()

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="ecommerce_db"
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

    total_amount = 0
    for item in order_request.cart:
        try:
            # Make a request to the Inventory service
            response = requests.get(f"http://localhost:8001/validate/{item.product_id}/{item.quantity}")
            print("Inventory service response:", response.json())

            
            if response.status_code != 200:
                print(f"Product {item.product_id} is out of stock.")
                raise HTTPException(status_code=400, detail=f"Product {item.product_id} out of stock.")

            response_data = response.json()
            total_amount += response_data['price'] * item.quantity
            print(f"Product {item.product_id} validated successfully. Total amount so far: {total_amount}")
        except Exception as e:
            print("Error while connecting to Inventory service:", str(e))
            raise HTTPException(status_code=500, detail=f"Failed to validate inventory: {str(e)}")


    order_id = next_order_id(cursor)

    try:
        cursor.execute("INSERT INTO orders (username) VALUES (%s, %s)", (order_request.username,total_amount,))
    

        for item in order_request.cart:
            cursor.execute("INSERT INTO ordered_products (order_id, product_id, quantity) VALUES (%s, %s, %s)", 
                           (order_id, item.product_id, item.quantity))
        

        db.commit()
        print("Order placed successfully")
        return {"message": "Order placed successfully", "order_id": order_id}

    except Exception as e:
        db.rollback()
        print("Error during order placement:", str(e))
        raise HTTPException(status_code=500, detail=f"Order placement failed: {str(e)}")

    finally:
        cursor.close()

@app.get("/")
def health_check():
    return {"status": "Order Service is running"}
