import random
from routers import users_router, channels_router, programs_router
from schemas import CreateProgramSchema


if __name__ == '__main__':
    
    users_router.db_collection.delete_many({})
    channels_router.db_collection.delete_many({})
    programs_router.db_collection.delete_many({})


    channels = 6

    for x in range(1,channels+1):
        channels_router.create({'title':f'Канал {x}'})

    for x in range(1,channels+1):
        channel = channels_router.db_collection.find_one({'title': f'Канал {x}'})
        for _ in range(1,7*channels+1):
            programs_router.create(
                CreateProgramSchema(
                    title=f'Програма {random.randint(1,99)}',
                    start_time=f'{str(random.randint(1,23)).zfill(2)}:00:00',
                    weekday=random.choice(
                            ['Monday', 'Tuesday',
                            'Wednesday', 'Thursday',
                            'Friday', 'Saturday', 'Sunday']
                        ),
                    channel_id=f"{channel['_id']}"
                )
            )
            
    users_router.create(
        {
            'email': 'admin@admin.com',
            'name': 'admin',
            'password': 'admin',
            'is_superuser': True
        }
    )
    
    users_router.create(
        {
            'email': 'user@user.com',
            'name': 'user',
            'password': 'user',
            'is_superuser': False
        }
    )