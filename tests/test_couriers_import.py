import requests


async def test_valid_post_data(rebuild_db_tables):
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

    r = requests.post("http://0.0.0.0:80/couriers", json=data)
    print(r.status_code)

    assert r.status_code == 201
    assert r.json() == {
        'couriers': [{'id': 1}, {'id': 2}, {'id': 3}]
    }


async def test_invalid_post_data(rebuild_db_tables):
    data = {"data": [

        {
            "courier_id": 2,
            "courier_type": "bike",
            "regionss": [22],
            "working_hours": ["09:00-18:00"]
        }]
    }

    r = requests.post("http://0.0.0.0:80/couriers", json=data)
    print(r.status_code)

    assert r.status_code == 400
    assert r.json() == {
        'validation_error': {
            'couriers': [{'id': 2}]
        }
    }


async def test_missing_field_in_post_data(rebuild_db_tables):
    data = {"data": [
        {
            "courier_id": 2,
            "regions": [22],
            "working_hours": ["09:00-18:00"]
        }]
    }

    r = requests.post("http://0.0.0.0:80/couriers", json=data)
    print(r.status_code)

    assert r.status_code == 400
    assert r.json() == {
        'validation_error': {
            'couriers': [{'id': 2}]
        }
    }


async def test_undeclared_field_in_post_data(rebuild_db_tables):
    data = {"data": [
        {
            "courier_id": 2,
            "regions": [22],
            "working_hours": ["09:00-18:00"],
            "sense_of_life": "undefined"
        }]
    }

    r = requests.post("http://0.0.0.0:80/couriers", json=data)
    print(r.status_code)

    assert r.status_code == 400
    assert r.json() == {
        'validation_error': {
            'couriers': [{'id': 2}]
        }
    }


async def test_replaced_field_in_post_data(rebuild_db_tables):
    data = {"data": [
        {
            "courier_id": 2,
            # "regions": [22],
            "working_hours": ["09:00-18:00"],
            "sense_of_life": "undefined"
        }]
    }

    r = requests.post("http://0.0.0.0:80/couriers", json=data)
    print(r.status_code)

    assert r.status_code == 400
    assert r.json() == {
        'validation_error': {
            'couriers': [{'id': 2}]
        }
    }


async def test_empty_post_data(rebuild_db_tables):
    data = {"data": [
    ]
    }

    r = requests.post("http://0.0.0.0:80/couriers", json=data)
    print(r.json())

    assert r.status_code == 201
    assert r.json() == {'couriers': []}
