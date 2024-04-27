from src.schemas import CreateChannelSchema
from .common import BaseRouter
from src.database import DB
from .programs import programs_router
from src.auth import is_superuser


class ChannelRouter(BaseRouter):
    db_collection = DB.channels
    
    @staticmethod
    def serialize(channel) -> dict:
        return {
            'id': str(channel['_id']),
            'title': channel['title'],
            'programs': programs_router.channel_listview(str(channel['_id']))
        }
        
    def create(self, program: CreateChannelSchema, is_superuser: is_superuser):
        return super().create(program, is_superuser)
    
    
channels_router = ChannelRouter(prefix='/channels', tags=['Channels'])