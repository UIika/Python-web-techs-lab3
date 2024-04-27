from bson import ObjectId
from fastapi import HTTPException
from src.schemas import CreateProgramSchema
from .common import BaseRouter
from src.database import DB
from src.auth import is_superuser


class ProgramRouter(BaseRouter):
    db_collection = DB.programs
    
    @staticmethod
    def serialize(program) -> dict:
        return {
            'id': str(program['_id']),
            'title': program['title'],
            'start_time': program['start_time'],
            'weekday': program['weekday'],
            'channel_id': str(program['channel_id']),
        }
        
    def create(self, program: CreateProgramSchema, is_superuser: is_superuser):
        try:
            channel = DB.channels.find_one({'_id': ObjectId(program.channel_id)})
        except:
            raise HTTPException(detail="Wrong channel id", status_code=400)
        if not channel:
            raise HTTPException(detail="Channel with such id does not exist", status_code=400)
        program.start_time = program.start_time.strftime('%H:%M')
        return super().create(program, is_superuser)
                
    
    def channel_listview(self, channel_id: str):
        return self.list_serialize(
            self.db_collection.find({'channel_id': channel_id}).sort("start_time", 1)
        )
    

programs_router = ProgramRouter(prefix='/programs', tags=['Programs'])