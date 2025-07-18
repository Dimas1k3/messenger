from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select 
from backend_python.auth.models import User

async def get_user_by_user_id(db: AsyncSession, user_id: str) -> User | None:
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()

async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    result = await db.execute(
        select(User).where(User.username == username)
    )
    return result.scalar_one_or_none()

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()

async def create_user(username: str, email: str, 
                      hashed_password: str, db: AsyncSession) -> User:
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        is_active=True 
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user