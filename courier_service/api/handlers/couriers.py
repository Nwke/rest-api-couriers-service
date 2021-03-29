from typing import List

from aiohttp import web

from courier_service.db.schema import Courier, async_session
from courier_service.api.handlers.base import BaseView
from courier_service.api.handlers.utils import validate_fields, does_courier_exists


class CouriersView(BaseView):
    """Import couriers"""
    URL_PATH = '/couriers'
    required_fields = ('courier_id', 'courier_type', 'regions', 'working_hours')

    async def post(self):
        response = await self.request.json()
        couriers_list = response['data']
        couriers_list: List[dict]

        invalid_data_in_post = False

        wrong_ids = []
        success_ids = []

        async with async_session() as session:

            for courier in couriers_list:
                given_fields_correct = validate_fields(self.required_fields, courier)

                if not given_fields_correct:
                    invalid_data_in_post = True
                    wrong_ids.append({"id": courier["courier_id"]})

                else:
                    courier_id = courier["courier_id"]
                    courier_type = courier["courier_type"]
                    regions = courier["regions"]
                    working_hours = courier["working_hours"]

                    instance = Courier(id=courier_id, type=courier_type, regions=regions,
                                       working_hours=working_hours,
                                       current_taken_weight=0)

                    success_ids.append({"id": courier["courier_id"]})
                    session.add(instance)

            if invalid_data_in_post:
                await session.rollback()
                body = {
                    'validation_error': {'couriers': wrong_ids}
                }
                return web.json_response(data=body, status=400)
            else:
                await session.commit()
                body = {
                    'couriers': success_ids
                }
                return web.json_response(data=body, status=201)
