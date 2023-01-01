from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, database, models

from jose import jwt , JWTError

from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from .. import schemas
from ..database import get_db

SECRET_KEY = "4409e7afebc4e68a921e45fbae56ef66acdff86b5188caa921546bb68b14b191"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt

router = APIRouter(
    tags = ["Login"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = db.query(models.Seller).filter(models.Seller.username==request.username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Username not found")
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Invalid Password")
    #Generate JWT token
    access_token = generate_token(
        data={"sub":user.username}
    )
    return {"access_token":access_token,
            "token_type":"bearer"
            }

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Auth Credentials",
        headers = {'WWW-Authentiacte':"Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        print("payload")
        print(payload)
        username:str = payload.get("sub")
        print(username)
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
        
    except JWTError:
        raise credentials_exception

