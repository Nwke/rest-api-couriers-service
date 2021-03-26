import requests
import asyncio
import json

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


async def sql_test():
    # id = Column(Integer, primary_key=True)
    # type = Column(String, nullable=False)
    # regions = Column(ARRAY(Integer), nullable=False)
    # working_hours = Column(ARRAY(String), nullable=False)
    # current_taken_weight = Column(Float, nullable=False, default=0)
    async with async_session.begin() as session:
        c = Courier(id=3, type="car", regions=[12],
                    working_hours=["18:00-19:00"], current_taken_weight=1)
        session.add(c)


def test_patch_req():
    data = {'working_hours_bitches!': ["14:00-15:30"]}
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
    data = {"courier_id": 1234}
    r = requests.post("http://localhost:8080/orders/assign", json=data)
    print(r)
    print(r.status_code)
    print(r.text)


if __name__ == '__main__':
    test_post_order_assign()
