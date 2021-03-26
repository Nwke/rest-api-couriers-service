from datetime import datetime

from sqlalchemy import select, update

from courier_service.api.handlers.base import BaseView
from courier_service.api.handlers.utils import containing_check, is_time_intersection, \
    CARRYING_CAPACITY
from courier_service.db.schema import Courier, Order, async_session

from aiohttp import web

import json


class OrderAssignView(BaseView):
    URL_PATH = '/orders/assign'
    required_fields = ('courier_id',)

    @staticmethod
    def get_appropriate_orders(courier: Courier, orders_list: list[Order]) -> list[Order]:
        suitable_regions = list(map(int, courier.regions))
        courier_time_intervals = courier.working_hours

        appropriate_orders_list = []

        for order in orders_list:
            if int(order.region) not in suitable_regions:
                continue

            found_suitable_order = False

            for order_time in order.delivery_hours:
                order_start, order_end = order_time.split('-')

                for time in courier_time_intervals:
                    courier_start, courier_end = time.split('-')
                    suitable_time_found = is_time_intersection(courier_start,
                                                               courier_end,
                                                               order_start,
                                                               order_end)
                    if suitable_time_found:
                        found_suitable_order = True

            if found_suitable_order:
                appropriate_orders_list.append(order)

        return appropriate_orders_list

    @staticmethod
    async def check_if_courier_exists(courier_id):
        async with async_session() as session:
            courier_select = select(Courier.id, Courier.type,
                                    Courier.regions,
                                    Courier.working_hours,
                                    Courier.current_taken_weight).where(
                Courier.id == int(courier_id))

            result = await session.execute(courier_select)
            courier_obj = result.first()
            if courier_obj is None:
                return False
            else:
                return True

    async def post(self):
        response = await self.request.json()

        async with async_session() as session:
            all_fields_valid = containing_check(
                OrderAssignView.required_fields, response)

            if not all_fields_valid:
                return web.Response(status=400, text='Bad Request: invalid field')

            elif all_fields_valid:
                # check if given courier id really exists
                courier_id = response['courier_id']

                courier_exists = await self.check_if_courier_exists(courier_id)

                if not courier_exists:
                    return web.Response(status=400, text='Bad Request: given not '
                                                         'existing courier id')

            # if post data are correct
            not_taken_orders_select = select(Order.id, Order.weight,
                                             Order.region,
                                             Order.delivery_hours).where(
                Order.taken == False).order_by(Order.weight)

            result = await session.execute(not_taken_orders_select)
            not_taken_orders_list = result.all()

            courier_id = response['courier_id']
            courier_select = select(Courier.id, Courier.type,
                                    Courier.regions,
                                    Courier.working_hours,
                                    Courier.current_taken_weight).where(
                Courier.id == int(courier_id))

            result = await session.execute(courier_select)
            courier = result.first()

            max_weight_for_courier = float(CARRYING_CAPACITY[str(courier.type)])

            t = datetime.utcnow().isoformat('T')
            t = t[:t.index('.') + 3] + 'Z'

            suitable_orders = OrderAssignView.get_appropriate_orders(courier,
                                                                     not_taken_orders_list)
            issued_orders_ids = []

            current_taken_weight = courier.current_taken_weight
            print('NICE ORDERS', suitable_orders)
            for order in suitable_orders:
                if float(current_taken_weight) + float(order.weight) <= \
                        max_weight_for_courier:
                    current_taken_weight += float(order.weight)

                    upd_stm = update(Order).where(Order.id == int(order.id)).values(
                        taken=True,
                        assign_time=t,
                        performing_courier=courier.id)

                    await session.execute(upd_stm)
                    issued_orders_ids.append({'id': order.id})

            upd_stm = update(Courier).where(Courier.id == int(courier.id)).values(
                current_taken_weight=current_taken_weight)

            await session.execute(upd_stm)

            await session.commit()

        body = {'orders': issued_orders_ids}
        # not empty order list
        if issued_orders_ids:
            body['assign_time'] = t

        return web.Response(status=200, text=json.dumps(body))
