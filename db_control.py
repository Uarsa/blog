from sqlalchemy import Text, create_engine, Table, Integer, String, Column, DateTime, MetaData
from datetime import datetime


metadata = MetaData()
engine = create_engine('sqlite:///clients.db')

table = Table(
    'article', metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', String(100)),
    Column('tel', String(20)),
    Column('type', String(10)),
    Column('device', String(100)),
    Column('description', Text()),
    Column('date', DateTime(), default=datetime.utcnow),
    Column('part_price', Integer()),
    Column('total_price', Integer()),
    Column('income', Integer())
    )

metadata.create_all(engine)
