import pytest
import requests

from courier_service.db.schema import main


async def test_valid_post_data(res):
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

    assert r.status_code == 201
    assert r.json() == {'description': 'created',
                        'content': {'couriers': [{'id': 1}, {'id': 2}, {'id': 3}]}}
