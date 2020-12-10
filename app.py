import os

from dotenv import load_dotenv
from flask import Flask, render_template, request
from models import (
    database, CarColors, Users, Cars
)
import peewee

app = Flask(__name__)
load_dotenv()

@app.before_request
def _db_connect():
    print('kalll')
    database.connect()

@app.teardown_request
def _db_close(_):
    if not database.is_closed():
        database.close()

@app.route('/')
def index():
    return render_template(
        'index.html'
    )

@app.route('/cars')
def cars():
    cars_query = (Cars.select(Cars.car_plate, Users.first_name, Users.last_name, Users.phone_number, CarColors.color_name)
                  .join(Users)
                  .join(CarColors, on=(Cars.color_id == CarColors.color_id)))
    carsList = list(cars_query.dicts())
    print(carsList)
    return render_template(
        'cars.html', carsList=carsList
    )

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
