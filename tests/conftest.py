import pytest
import asyncio

from courier_service.db.schema import Courier, Order, async_session, main
from sqlalchemy import delete


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def res():
    print('res start')
    async with async_session() as session:
        d1 = delete(Courier)
        d2 = delete(Order)
        await session.execute(d1)
        await session.execute(d2)

        await session.commit()
    return 5
