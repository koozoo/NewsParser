from sqlalchemy.future import select
from database.main import async_session_maker
from database.models.channel import Channel


async def delete_channel_by_id(channel_id: int):
    async with async_session_maker() as s:
        q = select(Channel).filter(Channel.id == channel_id)
        row = await s.execute(q)
        row = row.scalar_one()
        await s.delete(row)
        await s.commit()
