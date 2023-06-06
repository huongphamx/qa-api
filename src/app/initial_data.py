from asyncio import run

from app.db.init_db import init_db
from app.db.session import async_session


async def init():
    db = async_session()
    await init_db(db)
    await db.close()


if __name__ == "__main__":
    run(init())
