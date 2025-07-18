import asyncio
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from backend_python.config import DB_URL
from backend_python.chat.repository.user_repo import get_all_users

engine = create_async_engine(DB_URL, echo=False, pool_pre_ping=True)
SessionFactory = async_sessionmaker(engine, expire_on_commit=False)

redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

async def preload_all_users() -> None:
    async with SessionFactory() as db:
        user_list = await get_all_users(db) 

    pipe = redis_client.pipeline()
    for user_id, username in user_list:
        pipe.hset(
            f"user:{user_id}",
            mapping={
                "id": str(user_id),
                "username": username,
                "status": "offline",
            },
        )
        pipe.sadd("users_all", user_id)

    await pipe.execute()  

async def run_preload_all_users():
    print("Users loader worker started")
    await preload_all_users()
    print("Users loader worker finished")