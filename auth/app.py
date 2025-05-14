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
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (user.username, user.password))
    conn.commit()
    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: User):
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (user.username, user.password))
    if cursor.fetchone():
        redis_client.setex(user.username, 30, "loggedin")
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")