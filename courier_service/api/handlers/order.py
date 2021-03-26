import json

from courier_service.db.schema import Order, async_session

from courier_service.api.handlers.base import BaseView
from courier_service.api.handlers.utils import containing_check

from aiohttp import web


class OrderView(BaseView):
    URL_PATH = '/orders'
    required_fields = (
        'order_id', 'weight', 'region', 'delivery_hours')

    async def post(self):
        response = await self.request.json()
        orders_list = response['data']

        is_invalid_data = False
        wrong_ids = []
        success_ids = []

        async with async_session() as session:

            for order in orders_list:
                all_fields_exists = containing_check(
                    OrderView.required_fields, order)

                if not all_fields_exists:
                    is_invalid_data = True
                    wrong_ids.append({"id": order["order_id"]})

                else:
                    id = order["order_id"]
                    weight = order["weight"]
                    region = order["region"]
                    delivery_hours = order["delivery_hours"]

                    instance = Order(id=id, weight=weight, region=region,
                                     delivery_hours=delivery_hours)

                    success_ids.append({"id": order["order_id"]})
                    session.add(instance)

            if is_invalid_data:
                await session.rollback()
                body = json.dumps({'validation_error': {
                    'orders': wrong_ids
                }})
                return web.Response(body=body, status=400)
            else:
                await session.commit()
                body = json.dumps({'orders': success_ids})
                return web.Response(body=body, status=201)

    async def get(self):
        return web.Response(text=f'hello, guys from get req orders')
