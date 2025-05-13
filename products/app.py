from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import os
import mysql.connector
import redis

# Redis connection
redis_client = redis.Redis(host="redis-service", port=6379, decode_responses=True)

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
    username: str
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
def buy(req: BuyRequest):
    if not redis_client.exists(req.username):
        raise HTTPException(status_code=401, detail="Please login first")
    return {"message": f"User {req.username} bought product {req.product_id}"}
