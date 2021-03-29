from aiohttp import web
from sqlalchemy import select, update

from courier_service.db.schema import Courier, Order, async_session
from courier_service.api.handlers.base import BaseView
from courier_service.api.handlers.utils import (does_courier_exists,
                                                get_appropriate_orders_by_time_and_regions)
from courier_service.api.constants import CARRYING_CAPACITY


class CourierView(BaseView):
    """Update courier by id"""
    URL_PATH = r'/couriers/{courier_id:\d+}'

    async def patch(self):
        fields_to_modify = await self.request.json()
        courier_id = int(self.request.match_info['courier_id'])

        valid_fields = ['courier_type', 'regions', 'working_hours']

        async with async_session() as session:
            given_invalid_field = False

            for field in fields_to_modify:
                if field not in valid_fields:
                    print('Fuck', field)
                    given_invalid_field = True

            if given_invalid_field:
                body = {'description': 'Bad request'}
                return web.json_response(data=body, status=400)

            courier_exists = await does_courier_exists(courier_id, session)
            if not courier_exists:
                body = {'description': 'Not found'}
                return web.json_response(data=body, status=404)

            courier_update_stm = update(Courier).where(
                    Courier.id == int(courier_id)).values(**fields_to_modify)

            await session.execute(courier_update_stm)

            courier_select_stm = select(Courier.id, Courier.type, Courier.regions,
                                        Courier.working_hours,
                                        Courier.current_taken_weight).where(
                    Courier.id == int(courier_id))

            result = await session.execute(courier_select_stm)
            courier = result.first()

            await self.update_orders_due_to_courier_modification(courier, session)

            modified_courier = {
                'description': 'OK',
                'content': {
                    "courier_id": courier.id,
                    "courier_type": courier.type,
                    "regions": courier.regions,
                    "working_hours": courier.working_hours
                }}

            session.commit()
            return web.json_response(data=modified_courier, status=200)

    @staticmethod
    async def update_orders_due_to_courier_modification(courier: Courier,
                                                        session: async_session) -> None:
        """Because the patch method modify courier and this can make the courier
        unable to pass some orders. We should release these orders for others couriers """

        courier_id = int(courier.id)

        orders_select = select(Order.id, Order.region, Order.delivery_hours,
                               Order.weight).where(Order.performing_courier == courier_id)

        result = await session.execute(orders_select)
        orders_carried_by_courier = result.all()

        suitable_orders_by_time_and_region = get_appropriate_orders_by_time_and_regions(
                courier,
                orders_carried_by_courier)

        orders_to_release = []

        for carried_order in orders_carried_by_courier:
            if carried_order not in suitable_orders_by_time_and_region:
                orders_to_release.append(carried_order)

        released_weight = 0
        for order in orders_to_release:
            released_weight += float(order.weight)
            upd_stm = update(Order).where(int(Order.id) == int(order.id)).values(
                    taken=False,
                    assign_time=None,
                    performing_courier=None)

            await session.execute(upd_stm)

        print(courier, 'SUKA')

        new_taken_weight = courier.current_taken_weight - released_weight
        courier_update_stm = update(Courier).where(
                Courier.id == courier_id).values(
                current_taken_weight=new_taken_weight)

        await session.execute(courier_update_stm)

        max_weight = CARRYING_CAPACITY[courier.type]
        if new_taken_weight > max_weight:
            taken_orders_select = select(Order.id, Order.weight).where(
                    Order.performing_courier == courier_id).order_by((Order.weight))
            result = await session.execute(taken_orders_select)

            taken_orders = list(reversed(result.all()))

            i = 0
            while new_taken_weight > max_weight:
                order = taken_orders[i]
                i += 1
                upd_stm = update(Order).where(int(Order.id) == int(order.id)).values(
                        taken=False,
                        assign_time=None,
                        performing_courier=None)

                await session.execute(upd_stm)

                new_taken_weight -= float(order.weight)

            courier_update_stm = update(Courier).where(
                    Courier.id == courier_id).values(current_taken_weight=5)

            await session.execute(courier_update_stm)

        session.commit()
