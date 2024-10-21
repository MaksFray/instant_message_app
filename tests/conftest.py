from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src import metadata

from config import DB_USER_TEST, DB_HOST_TEST, DB_NAME_TEST, DB_PASS_TEST, DB_PORT_TEST

DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

engine_test = create_async_engine(DATABASE_URL_TEST, )
async_session_maker = async_sessionmaker(engine_test, expire_on_commit=False)

