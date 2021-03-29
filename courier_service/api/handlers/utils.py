from typing import List, Dict, Tuple

from sqlalchemy import select
from courier_service.db.schema import Courier, Order


def validate_fields(required_fields: Tuple, data: Dict):
    """it checks if given fields are correct correspond required_fields"""
    given_fields = data.keys()

    if len(set(given_fields)) != len(given_fields):
        return False

    if len(given_fields) != len(required_fields):
        return False

    diff = set(given_fields) - set(required_fields)
    if diff:
        return False

    return True


def is_time_intersection(courier_time, order_time):
    """It checks if courier is able to get order due to the desired time for order
    delivery"""

    courier_start, courier_end = courier_time.split('-')
    order_start, order_end = order_time.split('-')

    courier_start = int(courier_start.split(':')[0]) * 60 + int(
            courier_start.split(':')[1])
    courier_end = int(courier_end.split(':')[0]) * 60 + int(courier_end.split(':')[1])

    order_start = int(order_start.split(':')[0]) * 60 + int(order_start.split(':')[1])
    order_end = int(order_end.split(':')[0]) * 60 + int(order_end.split(':')[1])

    return courier_end >= order_end >= courier_start or order_end >= courier_end >= \
           order_start or courier_end >= order_end and courier_start <= order_start


async def does_courier_exists(courier_id, session):
    """It check if courier with given courier_id exists in database"""

    courier_select = select(Courier.id).where(
            Courier.id == int(courier_id))

    result = await session.execute(courier_select)
    courier_obj = result.first()

    if courier_obj is None:
        return False
    else:
        return True


def get_orders_suitable_by_region(courier: Courier, orders_list: List[Order]) -> \
        List[Order]:
    """return orders whose region destination hit in region courier working in"""

    courier_suitable_regions = list(map(int, courier.regions))

    appropriate_orders = []

    for order in orders_list:
        if int(order.region) in courier_suitable_regions:
            appropriate_orders.append(order)

    return appropriate_orders


def get_orders_suitable_by_time(courier: Courier, orders_list: List[Order]) -> \
        List[Order]:
    """return orders that satisfy the courier working hours i.e desired delivery time
    hit in the courier working hours"""

    courier_time_intervals = courier.working_hours

    appropriate_orders = []

    for order in orders_list:
        for order_time in order.delivery_hours:
            for courier_time in courier_time_intervals:
                suitable_time_found = is_time_intersection(courier_time, order_time)

                if suitable_time_found:
                    appropriate_orders.append(order)

    return appropriate_orders


def get_appropriate_orders_by_time_and_regions(courier: Courier,
                                               orders_list: List[Order]) -> List[
    Order]:
    orders_suitable_by_region = get_orders_suitable_by_region(courier,
                                                              orders_list)
    suitable_orders = get_orders_suitable_by_time(courier,
                                                  orders_suitable_by_region)

    return suitable_orders
