import json

from sqlalchemy import select, update

from courier_service.db.schema import Order, async_session
from courier_service.api.handlers.base import BaseView
from courier_service.api.handlers.utils import containing_check

from aiohttp import web


class OrderAssignView(BaseView):
    URL_PATH = '/orders/assign'
    required_fields = ('courier_id',)

    async def post(self):
        response = await self.request.json()

        async with async_session() as session:
            all_fields_valid = containing_check(
                OrderAssignView.required_fields, response)

            if not all_fields_valid:
                is_invalid_data = True

            else:
                not_taken_orders_select = select(Order.id, Order.weight,
                                                 Order.region,
                                                 Order.delivery_hours).where(
                    Courier.id == courier_id)
