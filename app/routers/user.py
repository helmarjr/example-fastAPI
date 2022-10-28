from .. import models, schemas, utils
from typing import List
from fastapi import HTTPException, APIRouter, Depends, status
from ..database import  get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix='/users',
    tags=['Users']
)

# ================== CREATE ==================1
@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ================== SELECT ==================
@router.get('', response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):  
    users = db.query(models.User).order_by(models.User.id).all()

    return users


@router.get('/{id}', response_model=schemas.User)
def get_user_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'user with id: {id} not found')

    return user


