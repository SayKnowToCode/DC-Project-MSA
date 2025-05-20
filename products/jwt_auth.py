# jwt_auth.py
import jwt
import os
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta

# JWT configuration
SECRET_KEY = os.environ["JWT_SECRET"]
ALGORITHM = os.environ["ALGORITHM"]
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")

# Utility function to create JWT token
def create_jwt_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# JWT token verification function
def verify_jwt_token(authorization: str = Depends(OAUTH2_SCHEME)):
    try:
        token = authorization
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
