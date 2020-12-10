from peewee import *
from dotenv import load_dotenv
from playhouse.shortcuts import model_to_dict
import psycopg2
import os
import prv

load_dotenv()

database = PostgresqlDatabase(
    os.environ['DATABASE'],
    user=os.environ['POST_USER'],
    password=os.environ['POST_PASS'],
    host=os.environ['POST_HOST'],
    port=os.environ['POST_PORT'],
)
#
# database = PostgresqlDatabase(
#     prv.DATABASE,
#     user=prv.USER,
#     password=prv.PASSWORD,
#     host=prv.HOST,
#     port=prv.PORT,
# )

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class CarColors(BaseModel):
    color_id = AutoField(primary_key=True)
    color_name = TextField()

    class Meta:
        table_name = 'carcolors'

class Users(BaseModel):
    first_name = TextField()
    last_name = TextField()
    phone_number = TextField()
    user_id = AutoField(primary_key=True)

    class Meta:
        table_name = 'users'

class Cars(BaseModel):
    car_plate = TextField(primary_key=True)
    color_id = ForeignKeyField(CarColors)
    user_id = ForeignKeyField(Users)

    class Meta:
        table_name = 'cars'

# database.drop_tables([CarColors, Cars, Users], cascade=True)

