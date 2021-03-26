CARRYING_CAPACITY = {'foot': 10, 'bike': 15, 'car': 50}


def containing_check(fields, data: dict):
    for field in fields:
        given_field = data.get(field, None)
        if given_field is None:
            return False
    return True


def is_time_intersection(courier_start, courier_end, order_start, order_end):
    courier_start = int(courier_start.split(':')[0]) * 60 + int(
        courier_start.split(':')[1])
    courier_end = int(courier_end.split(':')[0]) * 60 + int(courier_end.split(':')[1])

    order_start = int(order_start.split(':')[0]) * 60 + int(order_start.split(':')[1])
    order_end = int(order_end.split(':')[0]) * 60 + int(order_end.split(':')[1])

    return courier_end >= order_end >= courier_start or order_end >= courier_end >= \
           order_start or courier_end >= order_end and courier_start <= order_start
