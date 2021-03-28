from datetime import datetime

from aiohttp import web
from sqlalchemy import select, update

from courier_service.api.handlers.base import BaseView
from courier_service.api.handlers.utils import (validate_fields,
                                                does_courier_exists,
                                                get_appropriate_orders_by_time_and_regions)

from courier_service.api.constants import CARRYING_CAPACITY
from courier_service.db.schema import Courier, Order, async_session


class OrdersAssignView(BaseView):
    """Assign orders to a courier by id"""
    URL_PATH = '/orders/assign'
    required_fields = ('courier_id',)

    async def post(self):
        response = await self.request.json()
        data_in_post = response

        async with async_session() as session:
            all_fields_valid = validate_fields(self.required_fields, data_in_post)

            if not all_fields_valid:
                body = {'description': 'Bad request'}
                return web.json_response(data=body, status=400)

            # check if given courier id really exists
            courier_id = data_in_post['courier_id']
            courier_exists = await does_courier_exists(courier_id, session)

            if not courier_exists:
                body = {'description': 'Bad request'}
                return web.json_response(data=body, status=400)

            # if post data are correct
            not_taken_orders_select = select(Order.id, Order.weight,
                                             Order.region,
                                             Order.delivery_hours).where(
                    Order.taken == False and Order.complete_time is None).order_by(
                    Order.weight)

            result = await session.execute(not_taken_orders_select)
            not_taken_orders_list = result.all()

            courier_id = data_in_post['courier_id']
            courier_select = select(Courier.id, Courier.type,
                                    Courier.regions,
                                    Courier.working_hours,
                                    Courier.current_taken_weight).where(
                    Courier.id == int(courier_id))

            result = await session.execute(courier_select)
            courier = result.first()

            iso_time = datetime.utcnow().isoformat('T')
            iso_time = iso_time[:iso_time.index('.') + 3] + 'Z'

            suitable_orders = get_appropriate_orders_by_time_and_regions(courier,
                                                                         not_taken_orders_list)

            max_weight_for_courier = float(CARRYING_CAPACITY[str(courier.type)])
            current_taken_weight = courier.current_taken_weight

            for order in suitable_orders:
                if float(current_taken_weight) + float(order.weight) <= \
                        max_weight_for_courier:
                    current_taken_weight += float(order.weight)

                    upd_stm = update(Order).where(Order.id == int(order.id)).values(
                            taken=True,
                            assign_time=iso_time,
                            performing_courier=int(courier.id))

                    await session.execute(upd_stm)

            upd_stm = update(Courier).where(Courier.id == int(courier.id)).values(
                    current_taken_weight=current_taken_weight)

            await session.execute(upd_stm)

            await session.commit()

        issued_orders_select = select(Order.id, Order.assign_time).where(
                Order.taken == True and Order.performing_courier == int(
                    courier_id)).order_by(
                Order.id)

        result = await session.execute(issued_orders_select)
        issued_orders = result.all()

        body = self.formulate_response_body(issued_orders)

        return web.json_response(data=body, status=200)

    @staticmethod
    def formulate_response_body(issued_orders):
        orders_ids = [{"id": order.id} for order in issued_orders]
        body = {'description': 'OK',
                'content': {'orders': orders_ids}
                }

        # if not empty orders list
        if issued_orders:
            body['assign_time'] = issued_orders[0].assign_time

        return body
