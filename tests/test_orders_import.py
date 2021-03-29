import requests


async def test_valid_post_data(rebuild_db_tables):
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

    r = requests.post("http://0.0.0.0:80/orders", json=data)
    print(r.status_code)

    assert r.status_code == 201
    assert r.json() == {'description': 'Created',
                        'content': {'orders': [{'id': 1}, {'id': 2}, {'id': 3}]}
                        }


async def test_invalid_post_data(rebuild_db_tables):
    data = {"data": [
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
            "delivery_hours_bitch_wrong_field": ["09:00-12:00", "16:00-21:30"]
        }
    ]
    }

    r = requests.post("http://0.0.0.0:80/orders", json=data)
    print(r.status_code)

    assert r.status_code == 400
    assert r.json() == {'description': 'Bad request',
                        'content': {'validation_error': {
                            'orders': [{'id': 3}]
                        }}
                        }


async def test_invalid_multiple_post_data(rebuild_db_tables):
    data = {"data": [
        {
            "order_id": 2,
            # "weight": 0.11,
            "region": 1,
            "delivery_hours": ["09:00-18:00"]
        },
        {
            "order_id": 3,
            "weight": 0.01,
            "region": 22,
            "delivery_hours_bitch_wrong_field": ["09:00-12:00", "16:00-21:30"]
        }
    ]
    }

    r = requests.post("http://0.0.0.0:80/orders", json=data)
    print(r.status_code)

    assert r.status_code == 400
    assert r.json() == {'description': 'Bad request',
                        'content': {'validation_error': {
                            'orders': [{'id': 2}, {'id': 3}]
                        }}
                        }


async def test_missing_field_in_post_data(rebuild_db_tables):
    data = {"data": [
        {
            "order_id": 3,
            "weight": 0.01,
            # "region": 22,
            "delivery_hours": ["09:00-12:00", "16:00-21:30"]
        }]
    }

    r = requests.post("http://0.0.0.0:80/orders", json=data)
    print(r.status_code)

    assert r.status_code == 400
    assert r.json() == {'description': 'Bad request',
                        'content': {'validation_error': {
                            'orders': [{'id': 3}]
                        }}
                        }


async def test_undeclared_field_in_post_data(rebuild_db_tables):
    data = {"data": [
        {
            "order_id": 3,
            "weight": 0.01,
            "region": 22,
            "delivery_hours": ["09:00-12:00", "16:00-21:30"],
            "sense_of_life": "undefined"
        }]
    }

    r = requests.post("http://0.0.0.0:80/orders", json=data)
    print(r.status_code)

    assert r.status_code == 400
    assert r.json() == {'description': 'Bad request',
                        'content': {'validation_error': {
                            'orders': [{'id': 3}]
                        }}
                        }


async def test_replaced_field_in_post_data(rebuild_db_tables):
    data = {"data": [
        {
            "order_id": 3,
            "weight": 0.01,
            "delivery_hours": ["09:00-12:00", "16:00-21:30"],
            "sense_of_life": "undefined"
        }]
    }

    r = requests.post("http://0.0.0.0:80/orders", json=data)
    print(r.status_code)

    assert r.status_code == 400
    assert r.json() == {'description': 'Bad request',
                        'content': {'validation_error': {
                            'orders': [{'id': 3}]
                        }}
                        }


async def test_empty_post_data(rebuild_db_tables):
    data = {"data": [
    ]
    }

    r = requests.post("http://0.0.0.0:80/orders", json=data)
    print(r.status_code)

    assert r.status_code == 201
    assert r.json() == {'description': 'Created',
                        'content': {'orders': []}
                        }
