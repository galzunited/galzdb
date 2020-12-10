import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, flash, url_for
from models import (
    database, CarColors, Users, Cars
)
import peewee

app = Flask(__name__)
app.secret_key = 'super secret key'

load_dotenv()

def get_car_to_update():
    input_car_plate = request.form['input_car_plate']
    input_user_id = request.form['input_user_id']
    input_color_id = request.form['input_color_id']
    car_to_update = {Cars.car_plate: input_car_plate, Cars.user_id: input_user_id, Cars.color_id: input_color_id}
    return car_to_update

@app.before_request
def _db_connect():
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

@app.route('/users')
def users():
    users_query = Users.select()
    users = list(users_query.dicts())
    return render_template(
        'users.html', users=users
    )

@app.route('/delete_car/<car_plate>', methods=['POST'])
def delete_car(car_plate):
    print(car_plate)
    try:
        car_to_delete = Cars.get_by_id(car_plate)
        print('cartodelete', car_to_delete)
        car_to_delete.delete_instance()
        flash('Delete successfully.', 'danger')
    except:
        flash('Error delete car.', 'danger')

    return redirect(url_for('cars'))

@app.route('/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):
    print(user_id)
    try:
        user_to_delete = Users.get_by_id(user_id)
        user_to_delete.delete_instance()
        flash('Delete successfully.', 'success')
    except:
        flash('Couldnt delete user.', 'danger')
    return redirect(url_for('users'))

@app.route('/edit_car/<car_plate>', methods=['GET', 'POST'])
def edit_car(car_plate):
    if request.method == 'GET':
        cars_query = CarColors.select()
        car_colors = list(cars_query.dicts())
        users_query = Users.select()
        users = list(users_query.dicts())
        cars_query = (Cars.select(Cars.car_plate, Cars.user_id, Cars.color_id)
                      .where(Cars.car_plate == car_plate))
        car = list(cars_query.dicts())[0]
        return render_template(
            'edit_car.html', car=car, users=users, carColors=car_colors
        )
    elif request.method == 'POST':
        try:
            car_to_update = get_car_to_update()
            Cars.update(car_to_update).where(Cars.car_plate == car_plate).execute()
            flash('Updated car successfully.', 'success')
            return redirect(url_for('cars'))
        except:
            flash('Couldnt update car.', 'danger')
            return redirect(url_for('cars'))

@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    print('kan1', request.method)
    if request.method == 'GET':
        cars_query = CarColors.select()
        car_colors = list(cars_query.dicts())
        users_query = Users.select()
        users = list(users_query.dicts())
        return render_template(
            'add_car.html', carColors=car_colors, users=users
        )
    elif request.method == 'POST':
        print('kan')
        try:
            car_to_add = get_car_to_update()
            Cars.insert(car_to_add).execute()
            return redirect(url_for('cars'))
        except:
            return redirect(url_for('cars'))


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        users_query = Users.select()
        users = list(users_query.dicts())
        return render_template(
            'add_user.html', users=users
        )
    elif request.method == 'POST':
        print('kan')
        try:
            input_first_name = request.form['input_first_name']
            input_last_name = request.form['input_last_name']
            input_phone_number = request.form['input_phone_number']
            user_to_add = {Users.first_name: input_first_name, Users.last_name: input_last_name, Users.phone_number: input_phone_number}
            Users.insert(user_to_add).execute()
            flash('User was added successfully.', 'success')
            return redirect(url_for('users'))
        except:
            flash('Couldnt delete user - try deleting Cars related first', 'danger')
            return redirect(url_for('users'))



if __name__ == '__main__':
    app.run(threaded=True, port=5000)
