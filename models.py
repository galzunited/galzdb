from peewee import *

database = SqliteDatabase('cars.db')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class CarColors(BaseModel):
    color = BareField(null=True)
    color_id = AutoField(column_name='colorId')

    class Meta:
        table_name = 'carColors'

class Users(BaseModel):
    first_name = TextField()
    last_name = TextField()
    phone_number = TextField()
    user_id = AutoField(column_name='userId')

    class Meta:
        table_name = 'users'

class Cars(BaseModel):
    car_plate = TextField(primary_key=True)
    color = ForeignKeyField(column_name='colorId', field='color_id', model=CarColors, null=True)
    user = ForeignKeyField(column_name='userId', field='user_id', model=Users, null=True)

    class Meta:
        table_name = 'cars'

