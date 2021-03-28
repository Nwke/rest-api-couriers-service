import json

from aiohttp import web

from courier_service.db.schema import Order, async_session
from courier_service.api.handlers.base import BaseView
from courier_service.api.handlers.utils import validate_fields


class OrdersView(BaseView):
    """Import orders"""
    URL_PATH = '/orders'
    required_fields = (
        'order_id', 'weight', 'region', 'delivery_hours')

    async def post(self):
        response = await self.request.json()
        orders_list = response['data']
        orders_list: list[dict]

        invalid_data_in_post = False

        wrong_ids = []
        success_ids = []

        async with async_session() as session:

            for order in orders_list:
                given_fields_correct = validate_fields(OrdersView.required_fields, order)

                if not given_fields_correct:
                    invalid_data_in_post = True
                    wrong_ids.append({"id": order["order_id"]})

                else:
                    order_id = order["order_id"]
                    weight = order["weight"]
                    region = order["region"]
                    delivery_hours = order["delivery_hours"]

                    instance = Order(id=order_id, weight=weight, region=region,
                                     delivery_hours=delivery_hours)

                    success_ids.append({"id": order["order_id"]})
                    session.add(instance)

            if invalid_data_in_post:
                await session.rollback()
                body = {'description': 'Bad request',
                        'content': {'validation_error': {'orders': wrong_ids}}
                        }
                return web.json_response(data=body, status=400)
            else:
                await session.commit()
                body = {'description': 'created',
                        'content': {'orders': success_ids}
                        }
                return web.json_response(data=body, status=201)
