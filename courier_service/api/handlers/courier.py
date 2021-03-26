import json

from sqlalchemy import select, update

from courier_service.db.schema import Courier, async_session
from courier_service.api.handlers.base import BaseView

from aiohttp import web


class CourierView(BaseView):
    URL_PATH = r'/couriers/{courier_id:\d+}'

    async def patch(self):
        valid_fields = ['courier_type', 'regions', 'working_hours']
        response = await self.request.json()
        courier_id = int(self.request.match_info['courier_id'])

        async with async_session() as session:
            is_error = False

            for field in response:
                if field not in valid_fields:
                    is_error = True

            if not is_error:
                upd_stm = update(Courier).where(
                    Courier.id == courier_id).values(**response)

                await session.execute(upd_stm)

                await session.commit()

                sel_stm = select(Courier.id, Courier.type, Courier.regions,
                                 Courier.working_hours).where(
                    Courier.id == courier_id)

                result = await session.execute(sel_stm)
                user = result.first()
                modified_user = json.dumps({
                    "courier_id": user.id,
                    "courier_type": user.type,
                    "regions": user.regions,
                    "working_hours": user.working_hours
                })

                return web.Response(body=modified_user, status=200)

            else:
                await session.rollback()
                return web.Response(status=400, text='Bad Request: invalid '
                                                     'field')
