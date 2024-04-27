from datetime import datetime
from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.schemas import Weekday
from routers import users_router, channels_router, programs_router


app = FastAPI(
    title='lab3'
)


templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name="static")


for router in [users_router, channels_router, programs_router]:
    app.include_router(router, prefix='/api')


WEEKDAYS = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday',
} 


@app.get('/', tags=['Pages'])
async def home(
    request: Request,
    channels=Depends(channels_router.listview),
    weekday: Weekday = Weekday(WEEKDAYS[datetime.now().weekday()])
):
    return templates.TemplateResponse(
        'home.html',{'request': request,'channels': channels,'weekday': weekday}
    )