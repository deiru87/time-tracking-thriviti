from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from configuration.env import USER_DB, PASS_DB, NAME_DB, IP_SERVER, INSTANCE_NAME

if INSTANCE_NAME:
	DB_CONFIG = f"postgresql+asyncpg://" + USER_DB + ":" + PASS_DB + "@" + IP_SERVER + "/" + NAME_DB  +  "?host=" + INSTANCE_NAME 
else:
    DB_CONFIG = f"postgresql+asyncpg://" + USER_DB + ":" + PASS_DB + "@" + IP_SERVER + "/" + NAME_DB


class AsyncDatabaseSession:

    def __init__(self):
        self.session = None
        self.engine = None

    def __getattr__(self, name):
        return getattr(self.session, name)

    def init(self):
        self.engine = create_async_engine(DB_CONFIG, future=True, echo=True,pool_size=10, max_overflow=20)
        self.session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)()

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)


db = AsyncDatabaseSession()


async def commit_rollback():
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise