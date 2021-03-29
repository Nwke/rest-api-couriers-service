import requests


def test_valid_data_in_patch(rebuild_db_tables, import_couriers, import_orders):
    data = {
        "regions": [22]
    }

    r = requests.patch("http://localhost:8080/couriers/2", json=data)
    print(r.status_code)

    # assert r.status_code == 200
    assert r.json() == {'description': 'OK',
                        'content': {
                            "courier_id": 2,
                            "courier_type": "bike",
                            "regions": [22],
                            "working_hours": ["09:00-18:00"]}
                        }
