import smartcar
import googlemaps
from flask import Flask, redirect, request, jsonify, render_template, session
from flask_cors import CORS
from task import Task
from helpers import getVehicleFromId, getAddress, getTime, getDistance, getTimeAt
from datetime import datetime
import time

import os

app = Flask(__name__)
CORS(app)
app.secret_key = 'smartcar'
gmaps = googlemaps.Client(key='AIzaSyChhIkfCNJqOM7QYsBeQmOeG3LKE74RQa4')
start_coords = (43.663040, -79.398010)
# global variable to save our access_token
# access = None
print(os.environ.get('REDIRECT_URI'))


client = smartcar.AuthClient(
    client_id=os.environ.get('CLIENT_ID'),
    client_secret=os.environ.get('CLIENT_SECRET'),
    redirect_uri=os.environ.get('REDIRECT_URI'),
    scope=['read_vehicle_info','read_location', 'read_odometer','control_security', 'control_security:unlock', 'control_security:lock'],
    test_mode=True
)
@app.route('/', methods=['GET'])
def index():
    if 'access' not in session:
        return redirect('/login')
    else:
        return redirect('/dashboard')

@app.route('/login', methods=['GET'])
def login():
    auth_url = client.get_auth_url()
    return redirect(auth_url)

@app.route('/callback', methods=['GET'])
def callback():
    code = request.args.get('code')
    # in a production app you'll want to store this in some kind of
    # persistent storage
    global access_token
    access_token  = client.exchange_code(code);
    # session['access'] = client.exchange_code(code)
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    allTasks = []
    allTasks.append(Task('First Title', 111, 0, '10am', '12pm', 'destinationHERE', 'in progress'))
    allTasks.append(Task('Second Task', 112, 2, '1pm', '3pm', 'destinationHERE', 'not started'))

    return jsonify([task.getDict() for task in allTasks]), 200


@app.route('/vehicles')
def all():
    # if 'access' not in session:
    #     return redirect('/')

    access = access_token;
    vehicle_ids = smartcar.get_vehicle_ids(access['access_token'])['vehicles']

    newVehicles = []
    newVehicles.append({'id': 0, 'make': 'Buick', 'model': 'Cascada', 'year': 2018})
    newVehicles.append({'id': 1, 'make': 'Chevrolet', 'model': 'Bolt', 'year': 2019})
    newVehicles.append({'id': 2, 'make': 'Audi', 'model': 'A4 Sedan', 'year': 2018})

    allVehicles = list(map(lambda v: smartcar.Vehicle(v, access['access_token']).info(), vehicle_ids)) + newVehicles

    return jsonify(allVehicles), 200


@app.route('/vehicle/<id>', methods=['GET'])
def vehicleInfo(id):
    # if 'access' not in session:
    #     return redirect('/')

    access = access_token;

    # the list of vehicle ids
    result = getVehicleFromId(access, id);
    if not result:
        return redirect('/')
    else:
        return jsonify(result.info()), 200

@app.route('/vehicle/<id>/location')
def vehicleLocation(id):
    # if 'access' not in session:
    #     return redirect('/')

    access = access_token;
    vehicle = getVehicleFromId(access, id)
    if not vehicle:
        return redirect('/')
    else:
        location = vehicle.location()['data']
        return jsonify(getAddress(gmaps, location['latitude'], location['longitude'])), 200

@app.route('/vehicle/<id>/odometer')
def vehicleOdometer(id):
    # if 'access' not in session:
    #     return redirect('/')

    access = access_token;
    vehicle = getVehicleFromId(access, id)
    if not vehicle:
        return redirect('/')
    else:
        return jsonify(vehicle.odometer()), 200

@app.route('/vehicle/<id>/lock')
def vehicleLock(id):
    # if 'access' not in session:
    #     return redirect('/')

    access = access_token;
    vehicle = getVehicleFromId(access, id)
    if not vehicle:
        return redirect('/')
    else:
        return jsonify(vehicle.lock()), 200

@app.route('/vehicle/<id>/unlock')
def vehicleUnlock(id):
    # if 'access' not in session:
    #     return redirect('/')

    access = access_token;
    vehicle = getVehicleFromId(access, id)
    if not vehicle:
        return redirect('/')
    else:
        return jsonify(vehicle.unlock()), 200

@app.route('/destination')
def destination():
    # if 'access' not in session:
    #     return redirect('/')
    latitude = request.args.get('lat')
    longitude = request.args.get('lng')
    return jsonify(getAddress(gmaps, latitude, longitude)), 200

@app.route('/task/distance/')
def taskDistance():
    # if 'access' not in session:
    #     return redirect('/')
    latitude = request.args.get('lat')
    longitude = request.args.get('lng')

    return jsonify(getDistance(gmaps, start_coords, latitude, longitude)), 200

@app.route('/task/time')
def taskTime():
    # if 'access' not in session:
    #     return redirect('/')
    latitude = request.args.get('lat')
    longitude = request.args.get('lng')
    start_time = time.time()

    to_time = getTime(gmaps, start_coords, latitude, longitude)
    return_value = start_time + to_time['value']
    from_time = getTimeAt(gmaps, (latitude, longitude), start_coords[0], start_coords[1], return_value)

    timeDict = {}
    timeDict['to'] = to_time['text']
    timeDict['from'] = from_time['text']
    return jsonify(timeDict), 200

@app.route('/logout')
def logout():
    session.pop('access', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8080)
