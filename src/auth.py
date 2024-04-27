from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr


SECRET_KEY = 'lab3'
ALGORITHM = 'HS256'


bcrypt_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='api/users/token')


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(email: EmailStr, id: str, is_superuser: bool, expires_delta: timedelta):
    encode = {'sub': email, 'id': id, 'is_superuser': is_superuser}
    expires = datetime.now() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('id')
        email = payload.get('sub')
        is_superuser = payload.get('is_superuser')
        if not email or not user_id:
            raise HTTPException(status_code=401, detail='Could not validate user.')
        return {'id': user_id, 'email':email, 'is_superuser': is_superuser}
    except JWTError:
        raise HTTPException(status_code=401, detail='Could not validate user.')
    
def get_current_superuser(token: Annotated[str, Depends(oauth2_bearer)]):
    return get_current_user(token)['is_superuser']
    

is_authenticated = Annotated[dict, Depends(get_current_user)]
is_superuser = Annotated[dict, Depends(get_current_superuser)]