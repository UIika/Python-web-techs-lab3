from datetime import timedelta
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException

from src.auth import create_access_token, Token, bcrypt_context
from .common import BaseRouter
from src.database import DB
from src.schemas import CreateUserSchema
from src.auth import is_superuser


class UserRouter(BaseRouter):
    db_collection = DB.users
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_api_route('/token', self.login, methods=["POST"],
                                  response_model=Token, status_code=200)
    
    @staticmethod
    def serialize(user) -> dict:
        return {
            'id': str(user['_id']),
            'email': user['email'],
            'name': user['name'],
            'is_superuser': user['is_superuser'],
        }
        
    def create(self, user: CreateUserSchema):
        user = dict(user)
        if self.db_collection.find_one({'email': user['email']}):
            raise HTTPException(status_code=400, detail='User with such email already exists')
        if not user.get('is_superuser'):
            user['is_superuser'] = False
        user['password'] = bcrypt_context.hash(user['password'])
        user_dict = dict(user)
        self.db_collection.insert_one(user_dict)
        return {
            'Result': f'New user has been created successfully',
            'data': self.serialize(user_dict)
        }
    
    def update(self, id: str, user: CreateUserSchema, is_superuser: is_superuser):
        user.password = bcrypt_context.hash(user.password)
        return super().update(id, user, is_superuser)
    
    def login(self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        user = self.db_collection.find_one({'email': form_data.username})
        if not user or not bcrypt_context.verify(form_data.password, user['password']):
            raise HTTPException(status_code=400, detail='Wrong email or password')
        token = create_access_token(
            user['email'], str(user['_id']),
            user['is_superuser'], timedelta(minutes=60)
        )
        return {'access_token': token, 'token_type': 'bearer'}
    
    
users_router = UserRouter(prefix='/users', tags=['Users'])