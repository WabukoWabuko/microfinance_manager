from datetime import datetime, timedelta
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

def create_jwt(username: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode = {"sub": username, "exp": expire}
    return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
