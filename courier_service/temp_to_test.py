import requests
import asyncio
import json

import datetime

from sqlalchemy import select, update
from courier_service.db.schema import Courier, Order, async_session

from courier_service.db.schema import Courier, async_session


def test_post_spread_api():
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
    print(r.text)




def test_patch_req():
    data = {'working_hours': ["14:00-15:30"]}
    r = requests.patch("http://localhost:8080/couriers/3", json=data)
    print(r)
    print(r.status_code)
    print(r.text)


def test_post_req_order():
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


def test_post_order_assign():
    data = {"courier_id": 1}
    r = requests.post("http://localhost:8080/orders/assign", json=data)
    print(r)
    print(r.status_code)
    print(r.text)


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


if __name__ == '__main__':
    test_post_order_assign()
    #test_post_order_assign()

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(test_sess())
