from aiohttp import web

from sqlalchemy import select, update

from courier_service.db.schema import Courier, Order, async_session
from courier_service.api.handlers.base import BaseView
from courier_service.api.handlers.utils import validate_fields


class OrderCompleteView(BaseView):
    """Marks orders as completed"""
    URL_PATH = '/orders/complete'
    required_fields = ('courier_id', 'order_id', 'complete_time')

    async def post(self):
        response = await self.request.json()

        given_fields_correct = validate_fields(self.required_fields, response)

        if not given_fields_correct:
            body = {'description': 'Bad request'}
            return web.json_response(data=body, status=400)

        async with async_session() as session:
            courier_id = response['courier_id']
            order_id = response['order_id']
            complete_time = response['complete_time']

            select_stm = select(Order).where(Order.id == int(order_id) and
                                             Order.performing_courier == int(courier_id))
            result = await session.execute(select_stm)
            order_found = result.first()

            if not order_found:
                body = {'description': 'Bad request'}
                web.json_response(data=body, status=400)

            # if order is found that means data are correct
            upd_stm = update(Order).where(Order.id == int(order_id) and
                                          Order.performing_courier == int(
                    courier_id)).values(complete_time=complete_time)

            await session.execute(upd_stm)
            await session.commit()

        body = {'description': 'OK',
                'content': {'order_id': order_id}}
        return web.json_response(data=body, status=400)
