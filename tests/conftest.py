import requests
import pytest
import asyncio

from sqlalchemy import delete

from courier_service.db.schema import Courier, Order, async_session


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    return loop


@pytest.fixture
async def rebuild_db_tables():
    print('rebuild db start')
    async with async_session() as session:
        d1 = delete(Courier)
        d2 = delete(Order)
        await session.execute(d1)
        await session.execute(d2)

        await session.commit()
    print('rebuild db start')


@pytest.fixture
def import_couriers():
    print('IMPORT COURIERS')
    data = {"data": [
        {
            "courier_id": 1,
            "courier_type": "foot",
            "regions": [1, 12, 22],
            "working_hours": ["11:35-14:05", "09:00-11:00"]
        },
        {
            "courier_id": 2,
            "courier_type": "bike",
            "regions": [22],
            "working_hours": ["09:00-18:00"]
        },
        {
            "courier_id": 3,
            "courier_type": "car",
            "regions": [12, 22, 23, 33],
            "working_hours": []
        }]
    }

    r = requests.post("http://localhost:8080/couriers", json=data)


@pytest.fixture
def import_orders():
    print('ORDER IMPORT')
    data = {
        "data": [
            {
                "order_id": 1,
                "weight": 0.23,
                "region": 12,
                "delivery_hours": ["09:00-18:00"]
            },
            {
                "order_id": 2,
                "weight": 15,
                "region": 1,
                "delivery_hours": ["09:00-18:00"]
            },
            {
                "order_id": 3,
                "weight": 0.01,
                "region": 22,
                "delivery_hours": ["09:00-12:00", "16:00-21:30"]
            }]
    }

    r = requests.post("http://localhost:8080/orders", json=data)
