from fastapi import FastAPI, HTTPException, Depends, Request
import requests
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import os
import mysql.connector
from jwt_auth import create_jwt_token, verify_jwt_token
from datetime import timedelta
# Redis connection 
# import redis
# redis_client = redis.Redis(host="redis-service", port=6379, decode_responses=True)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

class Token(BaseModel):
    access_token: str
    token_type: str


# User registration
@app.post("/register")
def register(user: User):
    cursor.execute("SELECT * FROM users WHERE username = %s", (user.username,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="User already exists")

    try:
        # Step 1: Insert user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (user.username, user.password))
        conn.commit()

        # Step 2: Initialize cart via RPC
        json_rpc_payload = {
            "jsonrpc": "2.0",
            "method": "init",
            "params": {"username": user.username},
            "id": 1
        }
        response = requests.post("http://cart-service:6000/cart/init", json=json_rpc_payload)
        response_data = response.json()

        if "error" in response_data:
            # Rollback user creation if cart initialization fails
            cursor.execute("DELETE FROM users WHERE username = %s", (user.username,))
            conn.commit()
            raise HTTPException(status_code=500, detail="Cart initialization failed: " + response_data["error"]["message"])

        return {"message": "User registered and cart initialized successfully"}

    except Exception as e:
        # Rollback on general failure
        cursor.execute("DELETE FROM users WHERE username = %s", (user.username,))
        conn.commit()
        raise HTTPException(status_code=500, detail="Registration failed: " + str(e))

# User login
@app.post("/login", response_model=Token)
def login(user: User):
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (user.username, user.password))
    if cursor.fetchone():
        # Generate JWT token on successful login
        token = create_jwt_token({"username": user.username}, timedelta(hours=2))
        
        # redis_client.setex(user.username, 7200, "loggedin")
        
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Protected route to test token verification
@app.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    username = verify_jwt_token(token)
    return {"message": f"Hello, {username}. You are authorized!"}
