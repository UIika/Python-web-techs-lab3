from abc import ABC, abstractmethod
from typing import Collection
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel
from src.auth import is_superuser


class BaseRouter(APIRouter, ABC):
    db_collection: Collection

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_api_route('/list/', self.listview, methods=["GET"])
        self.add_api_route('/create/', self.create, methods=["POST"], status_code=201)
        self.add_api_route('/{id}/detail/', self.detail, methods=["GET"])
        self.add_api_route('/{id}/update/', self.update, methods=["PUT"], status_code=200)
        self.add_api_route('/{id}/patch/', self.patch, methods=["PATCH"], status_code=200)
        self.add_api_route('/{id}/delete/', self.delete, methods=["DELETE"], status_code=200)
    
    
    @staticmethod
    @abstractmethod
    def serialize():
        raise NotImplementedError
    
    def list_serialize(self, list):
        return [self.serialize(item) for item in list]
    
    
    
    def listview(self):
        return self.list_serialize(self.db_collection.find())
    
    def detail(self, id: str):
        try:
            model = self.db_collection.find_one({'_id': ObjectId(id)})
        except InvalidId:
            raise HTTPException(detail='Wrong id format', status_code=400)
        
        if not model:
            raise HTTPException(detail=f'{self.prefix[1:-1].capitalize()} not found', status_code=404)
        return self.serialize(model)
    
    def create(self, model, is_superuser: is_superuser):
        if not is_superuser:
            raise HTTPException(status_code=403, detail='You are not an admin')
        model_dict = dict(model)
        self.db_collection.insert_one(model_dict)
        return {
            'Result': f'New {self.prefix[1:-1]} has been created successfully',
            'data': self.serialize(model_dict)
        }
    
    def update(self, id: str, model: BaseModel, is_superuser: is_superuser):
        if not is_superuser:
            raise HTTPException(status_code=403, detail='You are not an admin')
        self.detail(id)
        self.db_collection.find_one_and_update(
            {'_id': ObjectId(id)},
            {'$set': dict(model)}
        )
        return {
            'Result': f'{self.prefix[1:-1].capitalize()} has been updated successfully',
            'data': dict(model)
        }
    
    def patch(self, id: str, model: dict, is_superuser: is_superuser):
        if not is_superuser:
            raise HTTPException(status_code=403, detail='You are not an admin')
        return self.update(id, model, is_superuser)
            
    def delete(self, id, is_superuser: is_superuser):
        if not is_superuser:
            raise HTTPException(status_code=403, detail='You are not an admin')
        model = self.detail(id)
        self.db_collection.delete_one({'_id': ObjectId(id)})
        return {
            'Result': f'{self.prefix[1:-1].capitalize()} has been deleted successfully',
            'data': dict(model)
        }