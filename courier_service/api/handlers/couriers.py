import json

from courier_service.db.schema import Courier, async_session
from courier_service.api.handlers.base import BaseView
from courier_service.api.handlers.utils import containing_check

from aiohttp import web


class CouriersView(BaseView):
    URL_PATH = '/couriers'
    required_fields = (
        'courier_id', 'courier_type', 'regions', 'working_hours')

    async def post(self):
        response = await self.request.json()
        courier_list = response['data']

        is_invalid_data = False

        wrong_ids = []
        success_ids = []

        async with async_session() as session:

            courier_list: list[dict]
            for courier in courier_list:

                all_fields_exists = containing_check(CouriersView.required_fields,
                                                     courier)

                if not all_fields_exists:
                    is_invalid_data = True
                    wrong_ids.append({"id": courier["courier_id"]})

                else:
                    id = courier["courier_id"]
                    type = courier["courier_type"]
                    regions = courier["regions"]
                    working_hours = courier["working_hours"]

                    instance = Courier(id=id, type=type, regions=regions,
                                       working_hours=working_hours,
                                       current_taken_weight=0)

                    success_ids.append({"id": courier["courier_id"]})
                    session.add(instance)

            if is_invalid_data:
                await session.rollback()
                body = json.dumps({'validation_error': {
                    'couriers': wrong_ids
                }})
                return web.Response(body=body, status=400)
            else:
                await session.commit()
                body = json.dumps({'couriers': success_ids})
                return web.Response(body=body, status=201)
