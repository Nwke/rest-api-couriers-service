import requests
from pprint import pprint
import asyncio
import json

import datetime

from sqlalchemy import select, update
from courier_service.db.schema import Courier, Order, async_session, engine, Base
from courier_service.api.app import create_app

from courier_service.db.schema import Courier, async_session


def test_import_couriers():
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
    print(r)
    print(r.status_code)
    print(r.json())


def test_patch_req():
    data = {'working_hours': ["14:00-15:30"]}
    r = requests.patch("http://localhost:8080/couriers/2", json=data)
    print(r)
    print(r.status_code)
    print(r.text)
    print(r.content)


def test_import_orders():
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
    print(r)
    print(r.status_code)
    print(r.text)
    print(r.content)


def test_orders_assign():
    data = {"courier_id": 1}
    r = requests.post("http://localhost:8080/orders/assign", json=data)
    print(r)
    print(r.text)
    print(r.ok)
    pprint(json.loads(r.text))


async def test_sess():
    async with async_session() as session:
        courier_id = 2
        courier_select = select(Courier.id, Courier.type,
                                Courier.regions,
                                Courier.working_hours,
                                Courier.current_taken_weight).where(
                Courier.id == int(courier_id))

        courier = await session.execute(courier_select)
        courier = courier.first()

        print(courier.type)


def reupdate_database():
    test_import_couriers()
    test_import_orders()


async def test_alchemy_features():
    async with async_session() as session:
        upd_stm = update(Order).where(Order.id == 2).values(weight=15)
        await session.execute(upd_stm)

        await session.commit()
    print('pizda')


async def test_sql_feature2():
    async with async_session() as session:
        sel_stm = select(Order).where(Order.id == 2)
        res = await session.execute(sel_stm)
        r = res.first()
        print('ARR', r)
        if r:
            print('HAH')

        await session.commit()
    print('pizda')


def test_order_complete():
    data = {"courier_id": 1}
    r = requests.post("http://localhost:8080/orders/complete", json=data)
    print(r)
    print(r.text)
    print(r.ok)


def an_test():
    data = {"data": [
        {
            "order_id": 5,
            "weight": 0.01,
            "region": 22,
            "delivery_hours": ["09:00-12:00", "16:00-21:30"],

        }]
    }

    r = requests.post("http://0.0.0.0:80/orders", json=data)
    print(r.status_code)


if __name__ == '__main__':

    an_test()

#    loop = asyncio.get_event_loop()
#   loop.run_until_complete(hyi())
# test_import_couriers()

# test_order_complete()


# reupdate_database()
# test_orders_assign()

# test_post_order_assign()

# loop = asyncio.get_event_loop()
# loop.run_until_complete(test_sess())
