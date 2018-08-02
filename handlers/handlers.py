from app import app
import motor.motor_asyncio
from sanic.exceptions import ServerError, SanicException
import sanic.response as response
import asyncio
from sanic_graphql import GraphQLView
from graphql.execution.executors.asyncio import AsyncioExecutor
from GraphQL_setup.schema import schema
import jwt
import os
from functools import wraps
from firebase_.firebase_db import upload_blob
import random


client = motor.motor_asyncio.AsyncIOMotorClient(
    'mongodb://Souldiv:ballsdeep78@ds145981.mlab.com:45981/heroku_hv9lg70l')
loop = asyncio.get_event_loop()


# GraphQl jwt middle Ware
async def protect_graph(next, root, info, **args):
    req = info.context['request']
    jwt_token = req.headers.get('authorization', None).split(' ')[1]
    req['jwt'] = jwt_token
    return_value = next(root, info, **args)
    return return_value


# Middleware
def protected(f):
    @wraps(f)
    def wrapper(request):
        jwt_token = request.headers.get(
            'authorization', None).split(' ')[1].rstrip()
        secret = os.environ.get('jwt_secret')
        decoded_token = jwt.decode(jwt_token, secret)
        print(decoded_token)
        try:
            if decoded_token['auth_level'] >= 3:
                return f(request)
            else:
                raise SanicException("Unauthorized Request", status_code=215)
        except KeyError:
            raise SanicException("Trampled jwt, investigate", status_code=217)
    return wrapper


# graphql initialization
@app.listener('before_server_start')
async def init_graphql(app, loop):
    app.add_route(GraphQLView.as_view(
        schema=schema,
        executor=AsyncioExecutor(loop=loop),
        graphiql=True,
        middleware=[protect_graph]), '/graphql')


# Non-GraphQL Routes
@app.route('/campaign', methods=['GET'])
async def sample_data(request):
    try:
        redirect_url = request.args['next'][0]
        print("REDIRECT URL ", redirect_url)
        document = {
            'fest_id': request.args['fest'][0],
            'campaign_id': request.args['cid'][0],
            'source': request.args['source'][0]
        }
    except KeyError:
        raise ServerError(
            "Key error, somebody trampled with the url", status_code=400)
    db = client['heroku_hv9lg70l']
    collection = db['campaign']
    collection.insert_one(document)
    return response.redirect(redirect_url)


@app.route('/upload', methods=['POST'])
@protected
async def upload_stuff(request):
    if request.files == {}:
        raise SanicException("No file provided", status_code=216)
    try:
        with open('temp/' + request.files['file'][0].name, 'wb') as f:
            f.write(request.files['file'][0].body)
    except KeyError:
        raise SanicException("Illegal filename", status_code=216)
    result = await upload_blob('temp/' + request.files['file']
                               [0].name, request.files['file'][0].name)
    if result:
        return response.json({
            'message': 'File successfuly uploaded',
            'status_code': '200'
        }, status=200)
    return response.json({
        'message': 'Problem with uploading file',
        'status_code': '500'
    }, status=500)
