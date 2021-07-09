from chalice import NotFoundError
from chalice import BadRequestError
import sys

from chalice import Chalice, Response
from urllib.parse import urlparse, parse_qs

# app = Chalice(app_name='api-rest')
app = Chalice(app_name='custom-response')
app.debug = True

CITIES_TO_STATE = {
    'seattle': 'WA',
    'portland': 'OR',
}

@app.route('/')
def index():
    return Response(body='hello world!',
                    status_code=200,
                    headers={'Content-Type': 'text/plain'})
# @app.route('/')
# def index():
#     return {'hello': 'world'}

@app.route('/', methods=['POST'],
           content_types=['application/x-www-form-urlencoded'])
def index():
    parsed = parse_qs(app.current_request.raw_body.decode())
    return {
        'states': parsed.get('states', [])
    }

@app.route('/cities/{city}')
def state_of_city(city):
    try:
        return {'state': CITIES_TO_STATE[city]}
    except KeyError:
        raise BadRequestError("Unknown city '%s', valid choices are: %s" % (
            city, ', '.join(CITIES_TO_STATE.keys())))

@app.route('/resource/{value}', methods=['PUT'])
def put_test(value):
    return {"value": value}

@app.route('/myview', methods=['POST', 'PUT'])
def myview():
    pass    


OBJECTS = {
}

@app.route('/objects/{key}', methods=['GET', 'PUT'])
def myobject(key):
    request = app.current_request
    if request.method == 'PUT':
        OBJECTS[key] = request.json_body
    elif request.method == 'GET':
        try:
            return {key: OBJECTS[key]}
        except KeyError:
            raise NotFoundError(key)

@app.route('/introspect')
def introspect():
    return app.current_request.to_dict()

