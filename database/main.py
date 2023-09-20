from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

import settings as config

DATABASE_URL = f"postgresql+asyncpg://{config.settings.database_.login}" \
                f":{config.settings.database_.pass_}" \
                f"@{config.settings.database_.host}" \
                f":{config.settings.database_.port}" \
                f"/{config.settings.database_.name}"

Base = declarative_base()

engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(engine,
                                   class_=AsyncSession,
                                   expire_on_commit=False)
