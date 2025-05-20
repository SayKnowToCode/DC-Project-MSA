# main.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import os
import mysql.connector
from jwt_auth import verify_jwt_token
# import redis

# Redis connection (optional, currently commented out)
# redis_client = redis.Redis(host="redis-service", port=6379, decode_responses=True)

app = FastAPI()

# MySQL connection
conn = mysql.connector.connect(
    host=os.environ["MYSQL_HOST"],
    user=os.environ["MYSQL_USER"],
    password=os.environ["MYSQL_PASSWORD"],
    database=os.environ["MYSQL_DB"],
    port=int(os.environ["MYSQL_PORT"]),
)
cursor = conn.cursor(dictionary=True)

class BuyRequest(BaseModel):
    product_id: int

@app.get("/getAll")
def get_all():
    cursor.execute("SELECT * FROM products")
    return cursor.fetchall()

@app.get("/getOne/{product_id}")
def get_one(product_id: int):
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return result

@app.post("/buy")
def buy(req: BuyRequest, username: str = Depends(verify_jwt_token)):
    # if not redis_client.exists(username):
    #     raise HTTPException(status_code=401, detail="Please login first")
    print(username)
    return {"message": f"User {username} bought product {req.product_id}"}
