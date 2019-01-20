import smartcar
from flask import Flask, redirect, request, jsonify,render_template
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# global variable to save our access_token
access = None

# TODO: Authorization Step 1a: Launch Smartcar authorization dialog
client = smartcar.AuthClient(
    client_id=os.environ.get('CLIENT_ID'),
    client_secret=os.environ.get('CLIENT_SECRET'),
    redirect_uri=os.environ.get('REDIRECT_URI'),
    scope=['read_vehicle_info','read_location','control_security'],
    test_mode=True,
)
@app.route('/',methods=['GET'])
def index():
   return render_template("index.html")


@app.route('/customerLogin',methods=['GET'])
def customerLogin():
   return render_template("login.html")

@app.route('/workerLogin',methods=['GET'])
def workerLogin():
   return render_template("employee.html")

@app.route('/login', methods=['GET'])
def login():
    # TODO: Authorization Step 1b: Launch Smartcar authentication dialog
    auth_url = client.get_auth_url()
    return redirect(auth_url)


@app.route('/exchange', methods=['GET'])
def exchange():
    # TODO: Authorization Step 3: Handle Smartcar response

    # TODO: Request Step 1: Obtain an access token
    code = request.args.get('code')

    print(code)

    global access
    # in a production app you'll want to store this in some kind of
    # persistent storage
    access = client.exchange_code(code)
    return '', 200


@app.route('/vehicle', methods=['GET'])
def vehicle():
    # TODO: Request Step 2: Get vehicle ids

    # TODO: Request Step 3: Create a vehicle

    # TODO: Request Step 4: Make a request to Smartcar API

    global access
    # the list of vehicle ids
    vehicle_ids = smartcar.get_vehicle_ids(
    access['access_token'])['vehicles']


    # TODO: Request Step 3: Create a vehicle
    # instantiate the first vehicle in the vehicle id list
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])

    info = vehicle.info()
    print(info)
    '''
    {
        "id": "36ab27d0-fd9d-4455-823a-ce30af709ffc",
        "make": "TESLA",
        "model": "Model S",
        "year": 2014
    }
    '''

    return jsonify(info), 200


if __name__ == '__main__':
    app.run(port=8000,debug=True)
