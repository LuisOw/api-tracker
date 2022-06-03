from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext


SECRET_KEY = "f6ca6d07ac8dc6564768c3b57dcdbcfdcdcfe71f6f7721c00fd0242c97d6ffd9"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_DAYS = 30


def encodeUser(id: str):
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    data_dict = dict()
    data_dict.update({"id": id})
    data_dict.update({"exp": expire})

    return jwt.encode(data_dict, SECRET_KEY, algorithm=ALGORITHM)


def decodeUser(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)


def verify_password(password: str, hashed_password: str, pwd_context: CryptContext):
    return pwd_context.verify(password, hashed_password)
