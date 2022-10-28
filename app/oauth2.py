from . import schemas, database, models
from jose import JWSError, jwt
from .config import settings
from fastapi import Depends, status, HTTPException
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi.security import OAuth2AuthorizationCodeBearer

oauth2_scheme = OAuth2AuthorizationCodeBearer(tokenUrl='login', authorizationUrl='')


SECRET_KEY = settings.auth_secret_key
ALGORITHM = settings.auth_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.auth_access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credetnials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")
        
        if not id:
            raise credetnials_exception

        token_data = schemas.TokenData(id=id)
    
    except JWSError:
        raise credetnials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credetnials_exception = HTTPException(  status_code=status.HTTP_401_UNAUTHORIZED, 
                                            detail='Could not validate credentials', 
                                            headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credetnials_exception) 

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
