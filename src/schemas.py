from datetime import datetime, time
from enum import Enum
from pydantic import BaseModel, ConfigDict, EmailStr


class Weekday(str, Enum):
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"


# USER//////////////////////////////////////////////////////////////////////////////////
class UserSchema(BaseModel):
    email: EmailStr
    name: str
    
    model_config = ConfigDict(from_attributes=True)

class ReadUserSchema(UserSchema):
    id: str
    is_superuser: bool

class CreateUserSchema(UserSchema):    
    password: str


# PROGRAM///////////////////////////////////////////////////////////////////////////////
class ProgramSchema(BaseModel):
    title: str
    start_time: time = datetime.now().strftime('%H:%M')
    weekday: Weekday
    channel_id: str
    
    model_config = ConfigDict(from_attributes=True)

class ReadProgramSchema(ProgramSchema):
    id: int
    
class CreateProgramSchema(ProgramSchema):
    pass


#CHANNEL//////////////////////////////////////////////////////////////////////////////////
class CreateProgramSchema(ProgramSchema):
    pass

class ChannelSchema(BaseModel):
    title: str
    
    model_config = ConfigDict(from_attributes=True)

class ReadChannelSchema(ChannelSchema):
    id: str
    programs: list[ReadProgramSchema]
    
class CreateChannelSchema(ChannelSchema):
    pass