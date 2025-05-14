from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import os
import mysql.connector
import redis
import requests
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
cursor = conn.cursor()

# Pydantic models
class User(BaseModel):
    username: str
    password: str

@app.post("/register")
def register(user: User):
    cursor.execute("SELECT * FROM users WHERE username = %s", (user.username,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="User already exists")

    try:
        # Step 1: Insert user
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (user.username, user.password))
        conn.commit()

        # Step 2: Initialize cart via RPC
        json_rpc_payload = {
            "jsonrpc": "2.0",
            "method": "init",
            "params": { "username" : user.username},
            "id": 1
        }

        response = requests.post("http://cart-service:6000/cart/init", json=json_rpc_payload)
        response_data = response.json()

        if "error" in response_data:
            # Optionally rollback the user creation if cart fails
            cursor.execute("DELETE FROM users WHERE username = %s", (user.username,))
            conn.commit()
            raise HTTPException(status_code=500, detail="Cart initialization failed: " + response_data["error"]["message"])

        return {"message": "User registered and cart initialized successfully"}

    except Exception as e:
        # General failure rollback (just in case)
        cursor.execute("DELETE FROM users WHERE username = %s", (user.username,))
        conn.commit()
        raise HTTPException(status_code=500, detail="Registration failed: " + str(e))


@app.post("/login")
def login(user: User):
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (user.username, user.password))
    if cursor.fetchone():
        redis_client.setex(user.username, 7200, "loggedin")
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")