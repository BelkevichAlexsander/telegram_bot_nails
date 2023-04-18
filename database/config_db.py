from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import config

# DB
engine = create_async_engine(
    config.db_connect.get_secret_value(),
    echo=True,
)

AsyncSessionLocal = async_sessionmaker(bind=engine, autocommit=False)
