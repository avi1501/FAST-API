from fastapi import APIRouter,status, Response, HTTPException
from fastapi.params import Depends

from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext

from .. import schemas, models
from ..database import get_db

router = APIRouter(
    tags = ["Signup"], 
    prefix = '/signup'
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

@router.post('/', response_model=schemas.DisplaySeller)
def signup(request:schemas.Seller, db: Session = Depends(get_db)):
    hashedPassword = pwd_context.hash(request.password)
    new_seller = models.Seller(username=request.username, email = request.email, password = hashedPassword)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller
