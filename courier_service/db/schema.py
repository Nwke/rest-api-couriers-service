import asyncio

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import ARRAY
from sqlalchemy import Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Courier(Base):
    __tablename__ = "Courier"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    regions = Column(ARRAY(Integer), nullable=False)
    working_hours = Column(ARRAY(String), nullable=False)
    current_taken_weight = Column(Float, nullable=False, default=0)


class Order(Base):
    __tablename__ = "Order"

    id = Column(Integer, primary_key=True)
    weight = Column(Float, nullable=False)
    region = Column(Integer, nullable=False)
    delivery_hours = Column(ARRAY(String), nullable=False)

    taken = Column(Boolean, nullable=False, default=False)
    assign_time = Column(DateTime, nullable=True)
    complete_time = Column(DateTime, nullable=True)
    performing_courier = Column(Integer, ForeignKey('Courier.id'),
                                nullable=True)


engine = create_async_engine(
    "postgresql+asyncpg://postgres:root@localhost/yandex_back_school",
    echo=True,
)

async_session = sessionmaker(
    engine, class_=AsyncSession
)


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
